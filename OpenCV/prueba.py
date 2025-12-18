import cv2
 
image1 = cv2.imread("arbol.png", cv2.IMREAD_COLOR) #BGR (Blue-Green-Red) format [1]
image2 = cv2.imread("arbol.png", cv2.IMREAD_GRAYSCALE) #Single Channel [0]
image3 = cv2.imread("arbol.png", cv2.IMREAD_UNCHANGED) #BGR-A (Blue-Green-Red-Alpha{opacity}) format [-1]
 
# Check if the image was loaded successfully
if image1 is None:
    print("Error: Image not found or unable to read.")
else:
    print("Image loaded successfully!")
if image2 is None:
    print("Error: Image not found or unable to read.")
else:
    print("Image loaded successfully!")
if image3 is None:
    print("Error: Image not found or unable to read.")
else:
    print("Image loaded successfully!")


# Display the image in a window
cv2.imshow("Displayed Image1", image1)
cv2.imshow("Displayed Image2", image2)
cv2.imshow("Displayed Image3", image3)

# Wait for a key press before closing the window
cv2.waitKey(0)
cv2.destroyAllWindows()