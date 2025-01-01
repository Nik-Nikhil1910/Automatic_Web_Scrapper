from flask import Flask, render_template, request
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
f_and_b_keywords = ['milk','cereal','yogurt','curd','baked','bakery','noodles','pasta','juice','beverages','shake','smoothies','kombucha','gummies','soups','dips','candy','candies','baby food']

dosage_keywords = ['capsule','sachet','tablet','powder','drinks','foods']

manufacturing_keywords = ['manufacturing','manufacture','r&d','research','development','biotechnology',"strain","cultivation","fermentation","encapsulation","microbial technology",'made','pharma','nutra','process']

brand_keywords = ["brands","private label manufacturing", "your logo here", "custom branding", "own brand solutions", "brand exclusivity", "market-ready products", "branded for your company", "tailored product lines","white label products","ready-to-brand","unbranded goods","label-ready packaging","off-the-shelf solutions"]

distributor_keywords = ["retailer", "channel partner", "product reseller", "logistics partner", "brand representative", "distribution partner", "supply chain partner", "trade distributor", "product broker", "stockist", "regional distributor", "global distributor", "market distributor", "wholesale distributor", "exclusive distributor", "distribution network", "trade partner", "distribution channel", "warehousing", "third-party distributor", "value-added distributor"]

probiotics_keywords=["probiotics", "live cultures", "friendly bacteria", "gut health", "microflora", "lactobacillus", "bifidobacterium", "saccharomyces boulardii", "prebiotics", "synbiotics", "health supplements", "gut-friendly", "digestive health", "live microorganisms", "beneficial bacteria", "flora balance", "bioactive cultures", "digestive aid", "probiotic strains", "probiotic-enriched", "probiotic-based", "microbial health", "probiotic supplements", "probiotic formula", "probiotic drink", "probiotic capsules", "probiotic yogurt", "probiotic powder", "lactobacillus acidophilus", "bifidobacterium bifidum", "lactobacillus rhamnosus", "lactobacillus casei", "bifidobacterium longum", "saccharomyces boulardii", "streptococcus thermophilus", "enterococcus faecium"]

fortification_keywords = ['enriched', 'enhanced','vitamin','vit', 'mineral', 'nutrient-dense', 'health-boosting', 'functional food', 'nutrient','nutrition','supplement','health supplementation','zinc','iron','magnesium','amino-acid','protien','omega-3','calcium','phosphorus']

brand_positioning_keywords= ['health','nutrition', 'supplement','vitamin','mineral','immune','wellness','diet','probiotics','gut','digestive','immunity','immune']

women_health_keywords = ['women','pcos','pcod','hormones','hormonal','female','iron','uti','urinary','bladder','urination']

gut_health_keywords= ['gut','digest','constipation','stool','inner-health','microbiome','bloating','intestine','intestinal','fiber']

cognitive_health_keywords= ['cognitive','brain health','memory','attentive','attentiveness','attention span','mental health','neuro',"dementia","alzheimer's", "parkinson's"]

sports_nutrition_keywords = ["muscle building", "athletic performance", "workout supplements", "post-workout recovery", "pre-workout formulas", "endurance supplements", "protein shakes", "recovery drinks", "sports fuel", "amino acid blends", "branched-chain amino acids (bcaas)", "protein isolate", "whey protein", "plant-based protein", "creatine supplementation", "beta-alanine", "hydration supplements", "energy gels", "sports hydration", "muscle recovery products", "sports recovery shakes", "high-performance protein", "electrolyte replenishment", "endurance energy", "strength training supplements", "fat-burning supplements", "post-exercise nutrition", "pre-workout boosters", "amino acid recovery", "sports nutrition powder", "weight loss supplements for athletes", "stamina boosters", "nutrient timing", "bodybuilding supplements", "sports performance optimization", "muscle endurance", "fatigue recovery", "high-intensity workout nutrition", "glycogen replenishment", "training supplementation", "energy-boosting formulas", "sports recovery drinks", "high-performance nutrition", "sports nutrition brands", "performance optimization"]


compatible_ingredients = ["fiber", "prebiotics", "vitamins", "minerals", "omega-3", "magnesium", "calcium", "collagen", "turmeric", "ginger", "garlic", "green tea extract", "zinc", "vitamin D", "vitamin C", "antioxidants", "amino acids", "protein", "glutamine", "L-carnitine", "branched-chain amino acids (BCAAs)", "quercetin", "flavonoids", "polyphenols", "green leafy vegetables", "yogurt", "fermented foods", "miso", "kimchi", "sauerkraut", "kefir", "kombucha","ice cream"]


viable_products = ['capsule', 'tablet', 'powder', 'sachet', 'gel', 'softgel', 'drink', 'food', 'chewable', 'bars', 'snack', 'functional food', 'fortified', 'enriched', 'smoothie', 'yogurt', 'dairy', 'protein', 'non-carbonated', 'non-alcoholic', 'bioactive', 'fortification', 'prebiotic', 'postbiotic', 'nutritional', 'dietary supplement', 'gut health', 'immune support', 'wellness', 'digestive health']

consumer_segment_keywords = ['health','wellness','nutrition','fitness','gut','immune','digest','nutrient','vitamin','mineral','diet','probiotic']
# Keyword categories
keyword_categories = {
    'Dosage': dosage_keywords,
    'Manufacturer': manufacturing_keywords,
    'Brand': brand_keywords,
    'Distributor': distributor_keywords,
    'F&B': f_and_b_keywords,
    'Probiotics': probiotics_keywords,
    'Fortification': fortification_keywords,
    'Brand Positioning': brand_positioning_keywords,
    "Women's Health": women_health_keywords,
    "Cognitive Health": cognitive_health_keywords,
    "Gut Health": gut_health_keywords,
    "Sports Nutrition": sports_nutrition_keywords,
    "Consumer Segment": consumer_segment_keywords,
    "Ingredient Usage": compatible_ingredients,
    "Viability": viable_products
}

# Helper functions (fetch_page_content, find_keywords)
def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')

def find_keywords(page_content, keywords):
    matches = [keyword for keyword in keywords if keyword in page_content.lower()]
    return matches

@app.route("/", methods=["GET", "POST"])
def index():
    final_op = {}
    if request.method == "POST":
        company_name = request.form["company_name"]
        company_url = request.form["company_url"]
        our_variables = {}

        try:
            if "http" in company_url:
                response = requests.get(company_url)
            else:
                company_url = "https://" + company_url
                response = requests.get(company_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                anchor_tags = soup.find_all('a', href=True)
                for tag in anchor_tags:
                    if any(keyword in tag.text.lower() for keyword in ["about", "product", "manufacturing", "brand", "brands","nutrition",'press']):
                        about_url = urljoin(company_url, tag['href'])
                        about_page_soup = fetch_page_content(about_url)
                        
                        for category, keywords in keyword_categories.items():
                            matches = find_keywords(about_page_soup.get_text(), keywords)
                            if matches:
                                our_variables[category] = matches
                                final_op[category] = 'Yes'

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        for feature in keyword_categories.keys():
            if feature not in final_op.keys():
                final_op[feature]= 'No'

        if final_op.get('Dosage') == 'Yes':
            final_op['Dosage'] = 'Compatible'
        else:
            final_op['Dosage'] = 'Incompatible'
        
        with open("log_file.log",'w') as file:
            file.write(f"the values that were matched to predict this output are: {our_variables}")

        return render_template('index.html', result=final_op)

    return render_template('index.html', result={})

if __name__ == "__main__":
    app.run(debug=True)
