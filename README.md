# **Content Flow: Content Optimization Platform**

---

## **About Us**

**Product Owners**
- Badrus Zaman, S.Kom., M.Cs. (PIC)
- Dr. Indra Kharisma Raharjana, S.Kom., M.T.

**Group 1 - Software Development Practicum I1**
- Alma Alya Cipta Putri (187221023)
- Anak Agung Ayu Bunga Kausalya (187221027)
- Fina Niswatin Nikmah (187221033)
- Evitadewi Nur Hakimah (187221070)
- Naufal Zaki Riyadi (187221074)

---

## **Application Description**
**Content Flow** is a web-based platform designed to help users enhance the quality of their digital content.  
The application utilizes Python-based *machine learning* algorithms to:  
- Automatically analyze content.  
- Provide content scoring based on various aspects.  
- Deliver actionable recommendations for quality improvement.

---

## **Key Features**
1. **Automatic Analysis**  
   - Provides a score based on content structure, keyword usage, and readability.  
2. **Improvement Recommendations**  
   - Offers specific suggestions to optimize content.

---

## **Technologies Used**
- **Backend Framework**: Django  
- **Analysis Algorithm**: Python with *machine learning* libraries  
- **Frontend**: HTML, CSS, and JavaScript  
- **Database**: No database (currently)  

---

## **How to Clone the Project from GitHub**
1. Copy the repository URL for Content Flow from the **Code** section.  
2. Open the folder where you want to save the project using *File Explorer*.  
3. Open the terminal in that folder by typing `cmd` in the search bar and pressing Enter.  
4. Run the following command in the terminal:  
   ```bash
   git clone <insert the GitHub URL you copied>
   ```
5. Wait until the cloning process is complete. The project will now be available in your chosen folder.

---

## **Steps to Install and Run the Application**
1. Ensure Python is installed on your computer.  
2. Open the Content Flow project in an editor such as VS Code.  
3. Install Django and other required libraries by running these commands in the terminal:  
   ```bash
   python -m pip install Django
   pip install django requests beautifulsoup4 nltk
   ```
4. Download the *stopwords* dataset for NLTK:  
   ```bash
   python
   import nltk
   nltk.download('stopwords')
   exit()
   ```
5. Run the local Django server using the following commands:  
   ```bash
   cd mysite
   python manage.py runserver
   ```
6. Open the application in your browser by typing `http://127.0.0.1:8000` or clicking the link displayed in the terminal.  
7. The Content Flow application is ready to use! 🎉

---

## **How to Use Content Flow**
1. **Navigate to the Landing Page**  
   - When you first open the application, you will see the landing page.  
2. **Start Content Analysis**  
   - Click the **"Analysis"** menu in the navigation bar.  
   - Enter the URL of the article or content you want to analyze in the form provided.  
3. **Analysis Process**  
   - Click the **"Analyze Now"** button and wait for a moment.  
4. **Analysis Results**  
   - The system will display the content quality score, analysis of key aspects, and suggestions for improvement.  

---

Thank you for using **Content Flow**! We hope this application helps you create better-optimized content. 🚀
