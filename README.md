# Streamlit-Portfolio
This repository is the source of:  
 https://anthony-vidales.streamlit.app/ 
a portfolio that showcases some of the skills of its creator, me.  

## Contact me
**Anthony Vidales**  
✉️ [Email](aspam314@protonmail.com)  
💼 [LinkedIn](https://www.linkedin.com/in/anthony-vidales-7a1681262/)  

## Navigation
On the web page there is a Home page that you will land on. To the left of the Home page there are other pages within to explore:  
```
├── Home
├── pages
   ├── 🪪 Who I Am
   ├── 🚗 Used Car Market Explorer
   ├── 📈 Car Market Dashboard
   └── ⌛ Upcoming Works
```

## Car Sales Dataset
**Vehicle Sales Data** can be found [here](https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data)  

Within this dataset there are 558837 rows with 16 columns

After the data was loaded in the env I did little data wrangling. Changed the sales date column to UTC format so pandas can use it, engineerd two new columns to help explore the relationships, removed outliers with the IQR method, and validated some of the columns becuase some if the values were non sense. I kept the NaN values until a method was used that needed them. 

## Requirements
Look at requirements.txt.  
If running locally install within a python vitual enviorment with:  
`pip install -r requirements.txt`

## AI Used
ChatGPT was used to assist in parts of this project. 
