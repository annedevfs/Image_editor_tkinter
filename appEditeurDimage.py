import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, PhotoImage
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import cv2




class FrontEnd:
    def __init__(self, fenetreFrontEnd):
        self.fenetreFrontEnd = fenetreFrontEnd   
        self.fenetreFrontEnd.title("Editeur d'images")

        self.logo = PhotoImage(file='logo.png').subsample(20,20)    #modifier le chemin


        self.fenetreFrontEnd.config(bg="#FFFFFF")
        self.hautDePage = tk.Frame(self.fenetreFrontEnd)
        self.hautDePage.pack()
        tk.Label(self.hautDePage,image=self.logo).grid(row=0,column=0,rowspan=2)
        tk.Label(self.hautDePage,text="Editeur d'images", font=('Cambria',17)).grid(row=0,column=1)  
        tk.Label(self.hautDePage,text='Vous pouvez importer une image et la modifier a votre gise.', font=('Cambria',13)).grid(row=2,column=1,sticky='nsew')


    #Conteneur principal elements
        self.menu = tk.Frame(self.fenetreFrontEnd, bg="#FFFFFF")
        self.menu.pack(padx=10,pady=4)
        self.menu.config(relief='raised', borderwidth=3, padx=20, pady=10)


        # EEE9E9
        tk.Button(self.menu, text='Téléverser 1', command=self.Televerser1, state=tk.NORMAL).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text='Téléverser 2', command=self.Televerser2).grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text='Conversion en niveaux de gris', command=self.ConversionNiveauxDeGris).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Image Originale", command=self.ImageOriginale).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Rotation", command=self.Rotation).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Ajuster la luminosité", command=self.AjusterLaLuminosite).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='sw')

        tk.Button(self.menu, text="Inversion des niveaux de gris", command=self.InversionNiveauxDeGris).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Conversion en noir et blanc", command=self.ConversionNoirBlanc).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Fusion de deux images", command=self.FusionDeuxImages).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Symétrie horizontale", command=self.SymetrieH).grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Symétrie verticale", command=self.SymetrieV).grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Filtres de couleur rouge", command=self.FiltreCouleurR).grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Filtres de couleur bleu", command=self.FiltreCouleurB).grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Filtres de couleur vert", command=self.FiltreCouleurV).grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Filtre médian", command=self.FiltreMedian).grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky='sw')
        tk.Button(self.menu, text="Tranposée", command=self.Transposee).grid(row=14, column=0, columnspan=2, padx=5, pady=5, sticky='sw')


        tk.Button(self.menu,text="Analyse de l'histogramme (image en niveaux de gris)",command=self.AnalyseHistogrammePourImgNivGris).grid(row=15, column=0, columnspan=2, padx=5,pady=5,sticky='sw')
        tk.Button(self.menu,text="Égalisation d'histogramme (image en niveaux de gris)",command=self.EgalisationHistogrammePourImgNivGris).grid(row=16, column=0, columnspan=2, padx=5,pady=5,sticky='sw')
        tk.Button(self.menu,text="Égalisation d'histogramme adaptative",command=self.EgalisationHistogrammeAdaptative).grid(row=17, column=0, columnspan=2, padx=5,pady=5,sticky='sw')
        tk.Button(self.menu,text="Égalisation d'histogramme (image couleur)",command=self.EgalisationHistogrammePourImgCouleur).grid(row=18, column=0, columnspan=2, padx=5,pady=5,sticky='sw')
        tk.Button(self.menu,text="Comparaison Égalisation d'histogramme et Égalisation d'histogramme adaptative (image couleur)",command=self.CompEgalHistogramme_EgalHistogrammeAdaptativePourImgCouleur).grid(row=19, column=0, columnspan=2, padx=5,pady=5,sticky='sw')
        tk.Button(self.menu,text="Filtrage spatial (avec Égalisation d'histogramme)",command=self.FiltrageSpatial).grid(row=20, column=0, columnspan=2, padx=5,pady=5,sticky='sw')
        tk.Button(self.menu,text="Ajustement de l'histogramme pour l'Amélioration du Contraste",command=self.AjustementHistogrammePourAmeliorationContraste).grid(row=21, column=0, columnspan=2, padx=5,pady=5,sticky='sw')


        # 1
        self.canvas = tk.Canvas(self.menu,width=600,height=400,bg='#FAF0E6')
        self.canvas.grid(row=0,column=2,rowspan=15)
        self.canvas2 = tk.Canvas(self.menu, width=600, height=400, bg='#FAF0E6')

        self.AppliquerSuppressionSauvegarde = tk.Frame(self.fenetreFrontEnd)
        self.AppliquerSuppressionSauvegarde.pack()
        tk.Button(self.AppliquerSuppressionSauvegarde, text='Supprimer les modifications', command=self.SupprimerModifications_Action).grid(row=19, column=4, columnspan=1, padx=5, pady=5, sticky='nsew')
        tk.Button(self.AppliquerSuppressionSauvegarde, text='Sauvegarder', command=self.Sauvegarder).grid(row=19, column=2, columnspan=1, padx=5, pady=5, sticky='nsew')



        self.imageActuelle1 = None  
        self.imageActuelle2 = None

        BoutonFusionImage = False
        AfficherHistogramme = False


    def Televerser1(self):      #OK
        self.NomFichier = askopenfile(title="Ouvrir une image")
        self.canvas.delete("all")
        if self.NomFichier:
            image = Image.open(self.NomFichier.name)
            largeurCanva = self.canvas.winfo_width()
            hauteurCanva = self.canvas.winfo_height()
            image = image.resize((largeurCanva, hauteurCanva), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo
            self.imageActuelle1 = photo


    def Televerser2(self):      #OK
        self.image2_Fusion = filedialog.askopenfilename(title="Sélectionnez la seconde image")
        self.canvas2.delete("all")
        if self.image2_Fusion:
            image = Image.open(self.image2_Fusion)

            largeurCanva = self.canvas2.winfo_width()
            hauteurCanva = self.canvas2.winfo_height()
            image = image.resize((largeurCanva, hauteurCanva), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.canvas2.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas2.image = photo
            self.imageActuelle2 = photo


    def SupprimerModifications_Action(self):      #OK
        if self.imageActuelle1:
            self.imageActuelle1 = Image.open(self.NomFichier.name)
            self.afficherImg(self.imageActuelle1)

        if self.imageActuelle2 :
            self.canvas2.delete("all")
            self.canvas2.destroy()
            self.canvas2 = tk.Canvas(self.menu, width=600, height=400, bg='#FAF0E6')


    def supAffichageHistogramme(self) :      #OK
        if self.imageActuelle2 and self.AfficherHistogramme == False :
            self.canvas2.delete("all")
            self.canvas2.destroy()
            self.canvas2 = tk.Canvas(self.menu, width=600, height=400, bg='#FAF0E6')


    def SupprimerHistFusion_Transposee(self):      #OK
            self.canvas2.delete("all")
            self.canvas2.destroy()
            self.canvas2 = tk.Canvas(self.menu, width=600, height=400, bg='#FAF0E6')



    def ConversionNiveauxDeGris(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            imageNivDeGris = imagePIL.convert('L')
            self.afficherImg(imageNivDeGris)

    def ImageOriginale(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            largeur, hauteur = imagePIL.size
            imageRedimensionnee = imagePIL.resize((largeur // 2, hauteur // 2))
            self.afficherImg(imageRedimensionnee)

    def Rotation(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            rotation = imagePIL.rotate(-90)  
            self.afficherImg(rotation)

    def AjusterLaLuminosite(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            imageAjustee = ImageEnhance.Brightness(imagePIL).enhance(1.3)  
            self.afficherImg(imageAjustee)

    def InversionNiveauxDeGris(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            imageGrise = imagePIL.convert("L")
            imageInversee = ImageOps.invert(imageGrise)
            self.afficherImg(imageInversee)


    def ConversionNoirBlanc(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            image = imagePIL.convert("L")
            seuil = 128
            image_nb = image.point(lambda x: 0 if x < seuil else 255)
            self.afficherImg(image_nb)


    def FusionDeuxImages(self):     #OK    
        self.SupprimerHistFusion_Transposee()
        self.BoutonFusionImage = True
    
        if self.imageActuelle2 and self.imageActuelle1 and self.BoutonFusionImage:
            image1 = Image.open(self.NomFichier.name)
            image2 = Image.open(self.image2_Fusion)

            image2 = image2.resize(image1.size)

            arrimg1 = np.array(image1)
            arrimg2 = np.array(image2)

            arrfusion = np.maximum(arrimg1, arrimg2)
            fusion = Image.fromarray(arrfusion)
            self.afficherImg(fusion)
   


    def SymetrieH(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            imageSymHorizontale = imagePIL.transpose(Image.FLIP_LEFT_RIGHT)
            self.afficherImg(imageSymHorizontale)

    def SymetrieV(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            imageSymVerticale = imagePIL.transpose(Image.FLIP_TOP_BOTTOM)
            self.afficherImg(imageSymVerticale)

    def FiltreCouleurR(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            r, g, b = imagePIL.split()
            r_img = Image.merge('RGB', (r, Image.new('L', r.size, 0), Image.new('L', r.size, 0)))
            self.afficherImg(r_img)

    def FiltreCouleurB(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            r, g, b = imagePIL.split()
            b_img = Image.merge('RGB', (Image.new('L', r.size, 0), Image.new('L', r.size, 0), b))
            self.afficherImg(b_img)

    def FiltreCouleurV(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            r, g, b = imagePIL.split()
            g_img = Image.merge('RGB', (Image.new('L', r.size, 0), g, Image.new('L', r.size, 0)))
            self.afficherImg(g_img)

    def FiltreMedian(self):      #OK
        self.AfficherHistogramme = False
        self.supAffichageHistogramme()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            tab_image = np.array(imagePIL)
            tab_filtre = ndimage.median_filter(tab_image, size=3)
            image_filtree = Image.fromarray(tab_filtre)
            self.afficherImg(image_filtree)


    def Transposee(self):      #OK 
        self.SupprimerHistFusion_Transposee()
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            transfImgEnTableau_image = np.array(imagePIL)
            if len(transfImgEnTableau_image.shape) == 3:
                tabTranspose = np.transpose(transfImgEnTableau_image, axes=(1, 0, 2))
            elif len(transfImgEnTableau_image.shape) == 2:
                tabTranspose = np.transpose(transfImgEnTableau_image, axes=(1, 0))
            else:
                print("Erreur: Dimensions d'image non prises en charge ou image vide.")
                return
            imageTransposee = Image.fromarray(tabTranspose)
            
            largeurCanva = self.canvas.winfo_width()
            hauteurCanva = self.canvas.winfo_height()
            image = imageTransposee.resize((largeurCanva, hauteurCanva), Image.LANCZOS)
            transposee = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=transposee)
            self.canvas.image = transposee




    def AnalyseHistogrammePourImgNivGris(self):      #OK
        self.BoutonAppuye = True
        if self.imageActuelle1 and self.BoutonAppuye :
            imagePIL = Image.open(self.NomFichier.name)
            imageGrise = imagePIL.convert("L")
            histogramme = imageGrise.histogram()
            self.afficherImg(imageGrise)

            plt.figure(figsize=(8, 6))
            plt.plot(histogramme, color='black')
            plt.title('Histogramme de l\'image en niveaux de gris')
            plt.xlabel('Intensité')
            plt.ylabel('Fréquence')
            plt.grid(True)
            
            nomHistogramme = "histogrammeImageCanvas2.png"
            plt.savefig(nomHistogramme)
            plt.close()
                
            hist = Image.open(nomHistogramme)
            self.afficherImgCanvas2(hist)



    def EgalisationHistogrammePourImgNivGris(self):      #OK 
        if self.imageActuelle1:
            imagePIL = Image.open(self.NomFichier.name)
            imgGrise = imagePIL.convert("L")
            imgEgalisee = ImageOps.equalize(imgGrise)
            histogramme = imgEgalisee.histogram() 
            self.afficherImg(imgEgalisee)

            plt.figure(figsize=(8, 6))
            plt.plot(histogramme, color='black')
            plt.title('Histogramme de l\'image en niveaux de gris')
            plt.xlabel('Intensité')
            plt.ylabel('Fréquence')
            plt.grid(True)
            
            nomHistogramme = "histogrammeImageCanvas2.png"
            plt.savefig(nomHistogramme)
            plt.close()
                
            hist = Image.open(nomHistogramme)
            self.afficherImgCanvas2(hist)



    def EgalisationHistogrammeAdaptative(self):
        if self.imageActuelle1:
            imgAdap = cv2.imread(self.NomFichier.name, cv2.IMREAD_GRAYSCALE)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            imgAdapEg = clahe.apply(imgAdap)

            histogrammeAvant = cv2.calcHist([imgAdap], [0], None, [256], [0, 256])
            plt.figure(figsize=(8, 6))
            plt.plot(histogrammeAvant, color='black')
            plt.title('Histogramme avant égalisation adaptative')
            plt.xlabel('Intensité')
            plt.ylabel('Fréquence')
            plt.grid(True)
            nomHistogrammeAvant = "histogrammeAvant.png"
            plt.savefig(nomHistogrammeAvant)
            plt.close()
            hist = Image.open(nomHistogrammeAvant)
            self.afficherImg(hist)

            histogrammeApres = cv2.calcHist([imgAdapEg], [0], None, [256], [0, 256])
            plt.figure(figsize=(8, 6))
            plt.plot(histogrammeApres, color='black')
            plt.title('Histogramme après égalisation adaptative')
            plt.xlabel('Intensité')
            plt.ylabel('Fréquence')
            plt.grid(True)
            nomHistogrammeApres = "histogrammeApres.png"
            plt.savefig(nomHistogrammeApres)
            plt.close()
            hist = Image.open(nomHistogrammeApres)
            self.afficherImgCanvas2(hist)



    def EgalisationHistogrammePourImgCouleur(self):      #OK
        if self.imageActuelle1:
            img = Image.open(self.NomFichier.name)
            img = img.convert("YCbCr")
            y, cb, cr = img.split()
            y_Eg = ImageOps.equalize(y)
            imgEgYcbcr = Image.merge("YCbCr", (y_Eg, cb, cr))
            self.afficherImg(imgEgYcbcr)
            imgYcbcrRgb = img.convert("RGB")
            self.afficherImgCanvas2(imgYcbcrRgb)



    def CompEgalHistogramme_EgalHistogrammeAdaptativePourImgCouleur(self): # OK
        if self.NomFichier.name:
            imgcouleur = cv2.imread(self.NomFichier.name)

            if imgcouleur is not None:
                imGrise = cv2.cvtColor(imgcouleur, cv2.COLOR_BGR2GRAY)
                filteSobel = cv2.Sobel(imGrise, cv2.CV_8U, 1, 1)
                sobelEgal = cv2.equalizeHist(filteSobel)

                plt.figure(figsize=(4.5, 3.5))
                plt.imshow(filteSobel, cmap='gray')
                plt.title('Image de bords avant égalisation d\'histogramme')
                plt.axis('off')
                plt.grid(True)
                nomHistogrammeAvant = "histogrammeEgAvant.png"
                plt.savefig(nomHistogrammeAvant)
                plt.close()
                hist = Image.open(nomHistogrammeAvant)
                self.afficherImg(hist)

                plt.figure(figsize=(5, 3))
                plt.imshow(sobelEgal, cmap='gray')
                plt.title('Image de bords après égalisation d\'histogramme')
                plt.axis('off')
                nomHistogrammeApres = "histogrammeEgApres.png"
                plt.savefig(nomHistogrammeApres)
                plt.close()
                hist = Image.open(nomHistogrammeApres)
                self.afficherImgCanvas2(hist)

            


    def FiltrageSpatial(self):      #OK
        if self.NomFichier.name:
            imageGrise = cv2.imread(self.NomFichier.name, cv2.IMREAD_GRAYSCALE)

            if imageGrise is not None:
                imgFiltree = cv2.GaussianBlur(imageGrise, (3, 3), 0)
                imgFiltreeSobel = cv2.Sobel(imgFiltree, cv2.CV_64F, dx=1, dy=1, ksize=5)
                image = Image.fromarray(imgFiltreeSobel.astype('uint8'))
                imageEg = ImageOps.equalize(image)
                self.afficherImg(image) 
                self.afficherImgCanvas2(imageEg)




    def AjustementHistogrammePourAmeliorationContraste(self):
        if self.NomFichier.name:
            imageGrise = cv2.imread(self.NomFichier.name, cv2.IMREAD_GRAYSCALE)
            
            plt.imshow(imageGrise)
            plt.axis('off')
            Initial = "imageInitial7.png"
            plt.savefig(Initial)
            plt.grid(True)
            plt.close()
            hist = Image.open(Initial)
            self.afficherImg(hist)
        
            plt.hist(imageGrise.flatten(), bins=256, color='black')
            plt.title('Histogramme initial')
            plt.xlabel('Intensité')
            plt.ylabel('Fréquence')
            nomHistogrammeInitial = "histogrammeInitial.png"
            plt.savefig(nomHistogrammeInitial)
            plt.grid(True)
            plt.close()
            hist = Image.open(nomHistogrammeInitial)
            self.afficherImgCanvas2(hist)


    def afficherImg(self, image=None):
        self.canvas.delete("all")
        if image is None:
            image = self.ImageEditee.copy()
        else:
            image = image.copy()
        self.ImageEditee = image

        largeurCanva = self.canvas.winfo_width()
        hauteurCanva = self.canvas.winfo_height()

        largeurImg, hauteurImg = image.size

        ratioImg = largeurImg / hauteurImg
        ratioCanva = largeurCanva / hauteurCanva

        if ratioImg > ratioCanva:
            largeurCanva = self.canvas.winfo_width()
            nouvelleHauteur = int(largeurCanva / ratioImg)
        else:
            hauteurCanva = self.canvas.winfo_height()
            nouvelleLargeur = int(hauteurCanva * ratioImg)

        image = image.resize((largeurCanva, hauteurCanva), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image=image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo
        self.imageActuelle1 = photo




    def afficherImgCanvas2(self, image=None):
        self.canvas2.delete("all")

        if image is None:
            image = self.ImageEditee.copy()
        else:
            image = image.copy()
        self.ImageEditee = image

        largeurCanva = self.canvas2.winfo_width()
        hauteurCanva = self.canvas2.winfo_height()

        largeurImg, hauteurImg = image.size

        ratioImg = largeurImg / hauteurImg
        ratioCanva = largeurCanva / hauteurCanva

        if ratioImg > ratioCanva:
            largeurCanva = self.canvas2.winfo_width()
            nouvelleHauteur = int(largeurCanva / ratioImg)
        else:
            hauteurCanva = self.canvas2.winfo_height()
            nouvelleLargeur = int(hauteurCanva * ratioImg)

        image = image.resize((largeurCanva, hauteurCanva), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image=image)

        self.canvas2.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas2.image = photo
        self.imageActuelle2 = photo
        self.canvas2.grid(row=13, column=2,rowspan=15)



    def Sauvegarder(self):
        if self.ImageEditee:
            nom_fichier = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")], title="Save Image As", initialfile="image.jpg")
            if nom_fichier:
                self.ImageEditee.save(nom_fichier)


if __name__ == "__main__"  :
    fenetrePrincipale = Tk()
    largeurFenetre = fenetrePrincipale.winfo_screenwidth()
    hauteurFenetre = fenetrePrincipale.winfo_screenheight()
    fenetrePrincipale.geometry(f"{largeurFenetre}x{hauteurFenetre}") 

    conteneurBackground = Canvas(fenetrePrincipale,bg='gray13', height=hauteurFenetre, width=largeurFenetre)

    back = Image.open("background.png")
    img = back.resize((largeurFenetre, hauteurFenetre), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    Imgbackground = tk.Label(fenetrePrincipale, image=img)
    Imgbackground.image=img
    Imgbackground.place(relx=0.5,rely=0.5, anchor='center')

    FrontEnd(fenetrePrincipale)
    fenetrePrincipale.mainloop()