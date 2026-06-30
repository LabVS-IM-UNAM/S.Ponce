from vispy import sys_info

print("===== VISPY SYSTEM INFO =====")
try:
    sys_info()  # <- funciona en VisPy >=0.14
except Exception as e:
    print("Error al ejecutar sys_info():", e)
print("=============================")
