import os
import numpy as np
import pandas as pd
import librosa

# Asegurar que parselmouth esté disponible
try:
    import parselmouth
    from parselmouth.praat import call
except ImportError:
    print("[ERROR] No se pudo importar 'praat-parselmouth'. Ejecuta: pip install praat-parselmouth")

def analizar_voz(audio_path, output_csv_path, fps=60):
    print(f"Cargando archivo: {audio_path}")
    
    # 1. Cargar audio con Librosa
    y, sr = librosa.load(audio_path, sr=None)
    duracion = librosa.get_duration(y=y, sr=sr)
    
    # Calcular hop_length exacto para los FPS de TouchDesigner
    hop_length = int(sr / fps)
    
    print(f"Duración: {duracion:.2f}s | Sample Rate: {sr}Hz | Sincronizando a {fps} FPS (Hop Length: {hop_length})")
    
    # Extracción temporal básica (RMS y Centroide)
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    frames_totales = len(rms)
    
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
    tiempos = librosa.frames_to_time(np.arange(frames_totales), sr=sr, hop_length=hop_length)
    
    # Arrays contenedores
    pitches = np.zeros(frames_totales)
    f1_formantes = np.zeros(frames_totales)
    f2_formantes = np.zeros(frames_totales)
    f3_formantes = np.zeros(frames_totales)
    
    # Valores Globales de Textura
    jitter_global = 0.0
    shimmer_global = 0.0
    hnr_global = 0.0
    
    try:
        # Cargar el audio en el motor de Praat
        sound = parselmouth.Sound(audio_path)
        
        # Extracción avanzada de Pitch (F0) y Formantes frame por frame calibrados
        pitch_obj = sound.to_pitch(time_step=1/fps)
        formant_obj = sound.to_formant_burg(time_step=1/fps)
        
        for i, t in enumerate(tiempos):
            p = pitch_obj.get_value_at_time(t)
            pitches[i] = p if not np.isnan(p) else 0.0
            
            f1 = formant_obj.get_value_at_time(1, t)
            f2 = formant_obj.get_value_at_time(2, t)
            f3 = formant_obj.get_value_at_time(3, t)
            
            f1_formantes[i] = f1 if not np.isnan(f1) else 0.0
            f2_formantes[i] = f2 if not np.isnan(f2) else 0.0
            f3_formantes[i] = f3 if not np.isnan(f3) else 0.0
            
        # =========================================================================
        # CORRECCIÓN DE MÉTRICAS GLOBALES (Praat estricto)
        # =========================================================================
        # 1. Crear el PointProcess vinculando Sound y Pitch (Método estándar de Praat)
        point_process = call([sound, pitch_obj], "To PointProcess (cc)")
        
        # 2. Jitter (local) SOLO acepta el objeto PointProcess seleccionado
        jitter_global = call(point_process, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)
        
        # 3. Shimmer (local) requiere AMBOS objetos seleccionados: Sound y PointProcess
        shimmer_global = call([sound, point_process], "Get shimmer (local)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
        
        # 4. Harmonicity (HNR) requiere el objeto Sound seleccionado
        harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 4.5)
        hnr_global = call(harmonicity, "Get mean", 0.0, 0.0)
        
        # Reemplazar NaNs por 0 en caso de silencios absolutos
        jitter_global = jitter_global if not np.isnan(jitter_global) else 0.0
        shimmer_global = shimmer_global if not np.isnan(shimmer_global) else 0.0
        hnr_global = hnr_global if not np.isnan(hnr_global) else 0.0
        
    except Exception as e:
        print(f"[ERROR/AVISO] Error en el motor de Praat: {e}")
        print("Se usará la aproximación básica de Librosa para Pitch.")
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), hop_length=hop_length)
        pitches = np.nan_to_num(f0)
        if len(pitches) < frames_totales:
            pitches = np.pad(pitches, (0, frames_totales - len(pitches)))
        else:
            pitches = pitches[:frames_totales]

    # 4. Construcción del Dataframe final
    data = {
        'Frame': np.arange(frames_totales),
        'Time_Seconds': tiempos,
        'Volumen_RMS': rms,
        'Pitch_F0': pitches,
        'Centroide_Espectral': spectral_centroid,
        'Formante_F1': f1_formantes,
        'Formante_F2': f2_formantes,
        'Formante_F3': f3_formantes,
        'Jitter_Global': [jitter_global] * frames_totales,
        'Shimmer_Global': [shimmer_global] * frames_totales,
        'HNR_Global': [hnr_global] * frames_totales
    }
    
    # Añadir los 13 MFCCs individuales
    for m in range(13):
        data[f'MFCC_{m+1}'] = mfcc[m]
        
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)
    print(f"¡Análisis completado exitosamente! Archivo guardado en: {output_csv_path}")
    print(f"Total de filas generadas: {len(df)}.")

if __name__ == '__main__':
    # Bloque de ejecución automática en lote (Mantiene tu estructura anterior)
    carpeta_entrada = "audios_limpios"
    carpeta_salida = "resultados_csv"

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"Carpeta creada: {carpeta_salida}")

    if not os.path.exists(carpeta_entrada):
        print(f"[ERROR] No se encontró la carpeta '{carpeta_entrada}'.")
    else:
        archivos_wav = [f for f in os.listdir(carpeta_entrada) if f.lower().endswith('.wav')]
        total_archivos = len(archivos_wav)
        print(f"Se encontraron {total_archivos} archivos .wav para procesar.\n")

        for indice, nombre_archivo in enumerate(archivos_wav, start=1):
            ruta_audio_completa = os.path.join(carpeta_entrada, nombre_archivo)
            nombre_csv = os.path.splitext(nombre_archivo)[0] + ".csv"
            ruta_csv_completa = os.path.join(carpeta_salida, nombre_csv)
            
            print(f"[{indice}/{total_archivos}] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            try:
                analizar_voz(ruta_audio_completa, ruta_csv_completa, fps=60)
            except Exception as e:
                print(f"[ERROR CRÍTICO] No se pudo procesar {nombre_archivo}: {e}")
            print("-" * 40)
            
        print("\n¡Proceso de lote finalizado! Todos los archivos CSV tienen sus métricas completas.")