##Bio page code, make changes for you
 
import streamlit as st
 
st.title("About me")
 
NAME = "Anthony Vidales"
PROGRAM = "Computer Scientist"
INTRO = (
    "I'm learning my way through computer science, mathematics, and philosophy, "
    "with a focus on how formal ideas can actually help in real-world situations."
)

PHIL = "If the visualizations "

SKILLS = [
    ("💻 Programming Languages", "Python, R, and Java for backend services, data pipelines, scripting, and academic projects."),
    ("🧮 Data Wrangling & Analysis", "Cleaning, joining, and standardizing multi-source CSV datasets; pivots, feature engineering, and exploratory data analysis in Python/R."),
    ("🧠 Machine Learning & Modeling", "Training and validating supervised and unsupervised models (linear/logistic regression, decision trees, KNN, neural networks, k-means clustering) with a focus on accuracy and interpretability."),
    ("📊 Data Visualization", "Building clear, interpretable plots and dashboards using matplotlib, ggplot2, Geospatial data and Plotly."),
    ("☁️ Cloud & AWS", "AWS Certified Cloud Practitioner; familiar with core AWS concepts (IAM basics, compute, storage) and interested in cloud infrastructure and data engineering workloads."),
    ("🐧 Linux & Servers", "Working with Ubuntu Server in a home lab, managing services, CLI workflows, and troubleshooting in a Linux environment."),
    ("📦 Containers & Deployment", "Containerizing applications with Docker and deploying microservices to platforms like Heroku as part of the SDLC."),
    ("⚙️ DevOps & CI/CD Concepts", "Understanding Git-based workflows, CI/CD ideas (build, test, deploy stages), and how pipelines support stable, repeatable releases."),
    ("📡 Networking & Infrastructure", "Hands-on experience with pfSense firewall, VLANs, VPN, DNS/DHCP, TCP/UDP fundamentals, and LAN/WAN concepts from both home lab and working in IT with an on prem environment."),

    ("🔐 Cybersecurity Fundamentals", "Grounding in core security concepts from (ISC)² CC, including the CIA triad, basic risk management, security controls, network security basics, incident response, and business continuity/disaster recovery principles."),
    ("🌐 Web APIs & Microservices", "Designing and consuming RESTful APIs; building microservices with Java Spring Boot and Python/Django, including ORM/data modeling."),
    ("🗄️ Databases & SQL", "Working with relational databases like PostgreSQL; writing SQL for queries, joins, and backing application data models."),
    ("🤖 Automation & Scripting", "Writing Python and Bash shell scripts to automate repetitive workflows."),
    ("🧰 Tools & Developer Practices", "Using Git/GitHub for version control, JUnit for testing, Agile/SDLC practices for iterative development, and general debugging/troubleshooting and many more."),
    ("📶 Active Directory & Identity", "Administering user and group accounts in Active Directory at the help desk level using ticket-driven workflows and least-privilege access."),
    ("📚 Accessibility & Documentation", "Documenting procedures and writing internal guides; creating WCAG-compliant process docs to improve accessibility of internal web content."),
    ("🪖 Leadership & Teamwork", "Leading a fire team in the U.S. Army, collaborating with cross-functional staff in IT support, and working as a reliable, detail-oriented teammate."),
    ("🗣️ Communication & Vendor Relations", "Communicating with vendors for equipment purchases, translating technical needs into clear requirements, and supporting non-technical stakeholders."),
]



photo_src = ('assets/headshot.jpg')
 
# -------------------- LAYOUT --------------------
col1, col2 = st.columns([1, 2], vertical_alignment="center")
 
with col1:
    st.image(photo_src, caption=NAME, use_container_width=True)
    st.markdown(
    """
        ✉️ [Email](aspam314@protonmail.com)  
        💼 [LinkedIn](https://www.linkedin.com/in/anthony-vidales-7a1681262/)  
        🐙 [GitHub](https://github.com/Anthony-Vdls)  
        🐍 [Leetcode](https://leetcode.com/u/user_3728198327/)  
        📜 [Credly](https://www.credly.com/users/anthony-vidales/)
    """
    )

st.divider()

with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)
    st.markdown(
            """
            > **Create clean, clear, compelling visuals so we can tell the whole story in a single glance**  
            > \- Me
            """
            )
st.markdown("### Skills Picked Up")
for title, desc in SKILLS:
    st.markdown(f'#### {title}')
    st.write(desc)

 
