from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

# Function to clean the file path input by removing quotes and doubling backslashes
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')  # Remove any surrounding quotes
    return cleaned_path.replace("\\", "\\\\")  # Double the backslashes

# Prompt user for .txt file location
file_input = input("Enter the full path to your text file: ")

# Clean the file path
txt_file = clean_file_path(file_input)

# Read the .txt file into a string
with open(txt_file, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Define additional stopwords (if any) and combine them with WordCloud's default stopwords
custom_stopwords = {'shall', 'unto', 'verily', 'thou', 'thy', 'therefore','thou art','thou shall','1','chapter','unto','saith','thus','came','let','paragraph','thence',
                     'forth','mine','dwell','saw','ever','like','indeed','along', 'rabbi','another','incident','said','rabbis','yehuda','rabban','kehuna','bar','ben',
                     'yosef','abba','shmuel','zakai','yehoshua','spoke','qed','52','ghayat','making','42','26','sghayat','9','made','18','back','36','51','proofs',
                     'see','v','even','noco','cicale','mada','zodiredo','odo','lape','hoathahe','qaa','od','zodoreje','zodacare','seem','come','thee','set', 'yet',
                     'may','hence', 'also','ye','upon','hath','go','saying','went','things','shalt','hast','till','place','call','would','stated','say','would',
                     'rather','well','etc','satanist', 'satanic','must','wilt','thine','neither','seeing','none','whatever','everywhere','called','comes','return',
                     'called','here','day','O','without','know','whole','comes','one','declared','goes','better','seen','act','now','filled','heard','sees','lived',
                     'take','beginning','become','tell','hear','best','offer','speak','never','dear','life','time','cause','rest','moving','regarding','many','others',
                     'regard','away','obtain','though','good','feet','cometh','less','fell','end','turned','much','done','thereof','turn','s','Wherefore','toward',
                     'spake','among','thing','art','put','taken','yea','lay','keep','surely','every','lest','took','told','doth','therein','left','gave','whose',
                     'shown','e','abide','concerning','named','able','course','set','asked','hold','thereon','give','either','consider','whether','make','behind',
                     'leaving','think','becomes','amongst','given','going','always','found','stanza','together','look','knows','live','us','find','clearly','led',
                     'little','speaks','known','instead','far','new','really','simply','according','merely','something','people','used','latter','various','kind',
                     'considered','killed','entire','appear','Similarly','Alternatively','nothing','read','placed','analogous','sent','Immediately','sit','began',
                     'sitting','certain','leave','midst','enter','anyone','derived','became','bring','already','mean','refer','refers','everyone','stood','Likewise',
                     'often','long','mere','everything','necessary','different','need','held','makes','holding','Additionally','especially','furthermore','example',
                     'although','consist','o','standing','z','consequently','Moreover','explain','want','x','Q','important','longer','might','Move','enough',
                     'allow','certainly','least','J','towards','Oh','anything','unless','non','later','will'}  # Add your own stopwords
stopwords = STOPWORDS.union(custom_stopwords)

# Function to generate and save word clouds with larger image size
def generate_wordcloud(text, title, filename):
    wordcloud = WordCloud(width=1600, height=800, background_color='white', stopwords=stopwords).generate(text)
    
    # Plot and save the word cloud
    plt.figure(figsize=(20, 10))  # Increase figure size
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    
    # Save the word cloud to the script's directory with higher DPI
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, filename)
    plt.savefig(output_file, dpi=300)  # Increase DPI for better resolution
    plt.close()

    print(f"Word cloud saved as: {output_file}")

# Generate and save word cloud for the entire text
generate_wordcloud(text_data, 'Quran Word Cloud', 'qur_wordcloud.png')
