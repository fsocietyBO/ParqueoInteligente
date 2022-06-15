import cv2
import imutils
import pytesseract
from PIL import Image

def sanearTexto(texto):
    letras = "ABCDEFGHIJQLMNOPQRSTUVWXYZ"
    numeros = "0123456789"
    aux = ""
    for i in texto:
        if i in letras:
            aux = aux + i
        elif i in numeros:
            aux = aux + i
    return aux


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
    image = cv2.imread('Placas/Placa8.jpeg', cv2.IMREAD_COLOR)
    image = imutils.resize(image, width=300)
    cv2.imshow("Imagen Original", image)
    cv2.waitKey(0)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("greyed image", gray_image)
    cv2.waitKey(0)

    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    cv2.imshow("smoothened image", gray_image)
    cv2.waitKey(0)

    edged = cv2.Canny(gray_image, 30, 200)
    cv2.imshow("edged image", edged)
    cv2.waitKey(0)

    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1=image.copy()
    cv2.drawContours(image1,cnts,-1,(0,255,0),3)
    cv2.imshow("contours",image1)
    cv2.waitKey(0)

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
    screenCnt = None
    image2 = image.copy()
    cv2.drawContours(image2,cnts,-1,(0,255,0),3)
    cv2.imshow("Top 30 contours",image2)
    cv2.waitKey(0)
    count = 0
    i=7
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx
            x,y,w,h = cv2.boundingRect(c)
            new_img=image[y:y+h,x:x+w]
            cv2.imwrite('./'+str(i)+'.png',new_img)
            i+=1
            break
    try:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        cv2.imshow("image with detected license plate", image)
    except Exception as e:
        print(e)

    cv2.waitKey(0)

    Cropped_loc = './7.png'
    cv2.imshow("cropped", cv2.imread(Cropped_loc))
    plate = pytesseract.image_to_string(Image.open(Cropped_loc), lang='eng', config='--psm 8') #8
    print("Number plate is:", plate)
    print("Texto saneado: ", sanearTexto(plate))
    cv2.waitKey(0)
    cv2.destroyAllWindows()