import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Post_Pandemic_Data as pdd
import Final_Visualization as fv

tech_and_computing = ["Computer and Information Systems Managers",
    "Computer Engineers (Except Software Engineers)",
    "Information Systems Analysts and Consultants",
    "Database Analysts and Data Administrators",
    "Software Engineers",
    "Computer Programmers and Interactive Media Developers",
    "Web Designers and Developers",
    "Computer and Network Operators and Web Technicians",
    "User Support Technicians",
    "Systems Testing Technicians"]

business_and_finance = ["Financial Auditors and Accountants",
    "Financial and Investment Analysts",
    "Securities Agents, Investment Dealers and Brokers",
    "Other Financial Officers",
    "Specialists in Human Resources",
    "Professional Occupations in Business Services to Management",
    "Professional Occupations in Public Relations and Communications",
    "Sales, Marketing and Advertising Managers",
    "Banking, Credit and Other Investment Managers",
    "Business Development Officers and Marketing Researchers and Consultants",
    "Insurance Agents and Brokers",
    "Loan Officers",
    "Technical Sales Specialists - Wholesale Trade",
    "Real Estate Agents and Salespersons"]

Science_Engineering_and_data = ["Physicists and Astronomers",
    "Chemists",
    "Geologists, Geochemists and Geophysicists",
    "Meteorologists",
    "Biologists and Related Scientists",
    "Civil Engineers",
    "Mechanical Engineers",
    "Electrical and Electronics Engineers",
    "Chemical Engineers",
    "Industrial and Manufacturing Engineers",
    "Metallurgical and Materials Engineers",
    "Mining Engineers",
    "Geological Engineers",
    "Petroleum Engineers",
    "Aerospace Engineers",
    "Other Professional Engineers, n.e.c.",
    "Mathematicians, Statisticians and Actuaries",
    "Natural and Applied Science Policy Researchers, Consultants and Program Officers",
    "Economists and Economic Policy Researchers and Analysts",
    "Supervisors, Electronics Manufacturing",
    "Supervisors, Electrical Products Manufacturing",
    "Central Control and Process Operators, Mineral and Metal Processing",
    "Petroleum, Gas and Chemical Process Operators",
    "Papermaking and Coating Control Operators",
    "Stationary Engineers and Auxiliary Equipment Operators",
    "Water and Waste Plant Operators",
    "Inspectors and Testers, Mineral and Metal Processing",
    "Chemical Plant Machine Operators",
    "Plastics Processing Machine Operators",
    "Rubber Processing Machine Operators and Related Workers",
    "Process Control and Machine Operators, Food and Beverage Processing",
    "Testers and Graders, Food and Beverage Processing",
    "Electronics Assemblers, Fabricators, Inspectors and Testers",
    "Assemblers and Inspectors, Electrical Appliance, Apparatus and Equipment Manufacturing",
    "Assemblers, Fabricators and Inspectors, Industrial Electrical Motors and Transformers",
    "Machine Operators and Inspectors, Electrical Apparatus Manufacturing"]

Health_and_medicine = ["Specialist Physicians",
    "General Practitioners and Family Physicians",
    "Dentists",
    "Veterinarians",
    "Optometrists",
    "Pharmacists",
    "Registered Nurses",
    "Medical Laboratory Technologists and Pathologists' Assistants",
    "Medical Laboratory Technicians",
    "Medical Radiation Technologists",
    "Medical Sonographers",
    "Cardiology Technologists",
    "Respiratory Therapists, Clinical Perfusionists and Cardio-Pulmonary Technologists",
    "Audiologists and Speech-Language Pathologists",
    "Physiotherapists",
    "Occupational Therapists",
    "Health Policy Researchers, Consultants and Program Officers",
    "Specialists in Clinical and Laboratory Medicine",
    "Specialists in Surgery"]

Education_and_research = ["University Professors",
    "Post-Secondary Teaching and Research Assistants",
    "College and Other Vocational Instructors",
    "Secondary School Teachers",
    "Elementary School and Kindergarten Teachers",
    "Education Policy Researchers, Consultants and Program Officers",
    "Librarians",
    "Archivists",
    "Editors",
    "Journalists",
    "Translators, Terminologists and Interpreters"]

Arts_media_Design = ["Authors and Writers",
    "Producers, Directors, Choreographers and Related Occupations",
    "Film and Video Camera Operators",
    "Graphic Arts Technicians",
    "Broadcast Technicians",
    "Audio and Video Recording Technicians",
    "Graphic Designers and Illustrators",
    "Interior Designers",
    "Theatre, Fashion, Exhibit and Other Creative Designers",
    "Conductors, Composers and Arrangers",
    "Musicians and Singers"]

Government_policy_socialscience = ["Social Policy Researchers, Consultants and Program Officers",
    "Program Officers Unique to Government",
    "Other Professional Occupations in Social Science, n.e.c.",
    "Lawyers and Quebec Notaries"]

df = fv.final_df
df["NOC_TITLE"].str.title()
tech_median_wages = list(df[df["NOC_TITLE"].isin(tech_and_computing)].groupby("Year")["MEDIAN_WAGE"].mean())
business_median_wages = list(df[df["NOC_TITLE"].isin(business_and_finance)].groupby("Year")["MEDIAN_WAGE"].mean())
sci_median_wages = list(df[df["NOC_TITLE"].isin(Science_Engineering_and_data)].groupby("Year")["MEDIAN_WAGE"].mean())
health_median_wages = list(df[df["NOC_TITLE"].isin(Health_and_medicine)].groupby("Year")["MEDIAN_WAGE"].mean())
Edu_median_wages = list(df[df["NOC_TITLE"].isin(Education_and_research)].groupby("Year")["MEDIAN_WAGE"].mean())
AMD_median_wages = list(df[df["NOC_TITLE"].isin(Arts_media_Design)].groupby("Year")["MEDIAN_WAGE"].mean())
Gov_median_wages = list(df[df["NOC_TITLE"].isin(Government_policy_socialscience)].groupby("Year")["MEDIAN_WAGE"].mean())
years = list(df["Year"].unique())

wages = [tech_median_wages, business_median_wages, sci_median_wages, health_median_wages, Edu_median_wages,
         AMD_median_wages, Gov_median_wages]
for year in years:
    print(df[df["Year"] == year].iloc[0])

for wage in wages:
    if len(wage) < len(years):
        for i in range(len(years)-len(wage)):
            wage.append(np.nan)

plt.scatter(x=years, y=tech_median_wages, color='blue', label = "Technology & Computing", alpha = 0.5)
plt.scatter(x=years, y=business_median_wages, color='yellow', label = "Business, Finance & Management", alpha = 0.5)
plt.scatter(x=years, y=sci_median_wages, color='cyan', label = "Science, Engineering & Data", alpha = 0.5)
plt.scatter(x=years, y=health_median_wages, color='red', label = "Health & Medicine", alpha = 0.5)
plt.scatter(x=years, y=Edu_median_wages, color='yellow', label = "Education & Research", alpha = 0.5)
plt.scatter(x=years, y=AMD_median_wages, color='purple', label = "Arts, Media & Design", alpha = 0.5)
plt.scatter(x=years, y=Gov_median_wages, color='olive', label = "Government, Policy & Social Science", alpha = 0.5)
plt.legend()
plt.title("Median Wages of AI Related Jobs From the Last Decade")
plt.xlabel("Years")
plt.ylabel("Median Wages")
plt.show()