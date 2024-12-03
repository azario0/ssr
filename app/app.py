from flask import Flask, render_template, request, redirect, url_for
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import random

app = Flask(__name__)

# Set up Gemini AI LLM
os.environ["GOOGLE_API_KEY"] = 'YOUR_API_KEY'
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Recipe data
recipes = {
    'Classic_Sushi_Rolls': {
        "Name":"Classic Sushi Rolls",
        "Short Description":  """Fresh and delicate sushi rolls made with rice, seaweed, and your choice of fillings like cucumber, avocado, and crab meat.""",
            'Full Description':"Sushi rolls, or 'maki,' are a beloved Japanese dish that consists of vinegared rice combined with various fillings, all rolled up in seaweed (nori). This recipe will guide you through making a basic sushi roll with cucumber, avocado, and crab meat, but feel free to get creative with your favorite ingredients.",
            'Ingredients':"""
        2 cups sushi rice

        2 cups water

        1/4 cup rice vinegar

        2 tablespoons sugar

        1 teaspoon salt

        4 sheets of nori (seaweed)

        1 cucumber, thinly sliced

        1 avocado, peeled and sliced

        1/2 cup crab meat (real or imitation)

        Wasabi and soy sauce for serving""",
            'How to Cook':"""
        Rice: Rinse the rice until the water runs clear. Combine rice and water in a pot, bring to a boil, then reduce heat to low, cover, and simmer for 18-20 minutes. Remove from heat and let it steam for another 10 minutes.
        Vinegar Mixture: In a small pan, combine rice vinegar, sugar, and salt. Heat until the sugar dissolves.
        Cool Rice: Spread the cooked rice on a large plate and pour the vinegar mixture over it. Gently mix with a wooden spoon.
        Rolling: Place a sheet of nori on a sushi mat, shiny side down. Spread a thin layer of rice over the nori, leaving a 1-inch border at the top. Arrange cucumber, avocado, and crab meat in a line across the center.
        Roll: Lift the bottom edge of the mat and roll forward, pressing gently to form a tight roll. Repeat with remaining ingredients.
        Slice: Using a sharp knife, slice the rolls into 8 pieces each. Serve with wasabi and soy sauce.
        """,
            'Facts':['Sushi originated in Japan, but it has become popular worldwide.,'
        'Traditional sushi was developed as a way to preserve fish, but it has evolved into an art form.',
        "Sushi is often eaten with chopsticks, and it’s customary to dip the sushi into soy sauce with the fish side, not the rice side."]

        },
    'Quinoa_Salad_with_Roasted_Vegetables': {
                "Name":"Quinoa Salad with Roasted Vegetables",
        "Short Description":  """A healthy and flavorful quinoa salad packed with roasted vegetables, chickpeas, and a tangy dressing.""",
            'Full Description':"This quinoa salad is a nutritious and delicious dish that can be enjoyed as a main course or side. It combines cooked quinoa with a variety of roasted vegetables, chickpeas, and a zesty lemon-tahini dressing. It’s perfect for meal prep or a light lunch.",
            'Ingredients':"""
        1 cup quinoa, uncooked

        2 cups water or vegetable broth

        2 cups mixed vegetables (e.g., bell peppers, zucchini, cherry tomatoes, onions), chopped

        1/2 cup chickpeas, cooked

        1/4 cup chopped fresh parsley

        1/4 cup chopped fresh mint

        1/4 cup lemon juice

        3 tablespoons tahini

        1 tablespoon olive oil

        1 clove garlic, minced

        Salt and pepper to taste
        """,
            'How to Cook':"""
        Cook Quinoa: Rinse the quinoa under cold water. In a medium pot, combine quinoa and water or broth. Bring to a boil, then reduce heat to low, cover, and simmer for 15-20 minutes, or until the quinoa is cooked and the liquid is absorbed.

        Roast Vegetables: Preheat the oven to 400°F (200°C). Toss the chopped vegetables with a little olive oil, salt, and pepper on a baking sheet. Roast for 20-25 minutes, or until tender and slightly caramelized.

        Make Dressing: In a small bowl, whisk together lemon juice, tahini, olive oil, garlic, salt, and pepper until smooth.

        Assemble Salad: In a large bowl, combine the cooked quinoa, roasted vegetables, chickpeas, parsley, and mint. Pour the dressing over the top and toss to combine.

        Serve: Serve at room temperature or chill in the refrigerator before serving.
        """,
            'Facts':["Quinoa is a complete protein, making it a great option for vegetarians and vegans.",
                    "This dish is highly customizable—feel free to add or substitute your favorite vegetables or proteins.",
                    "Quinoa salad is popular in many cuisines, including Middle Eastern, Mediterranean, and Latin American."]
            },
    'Beef_Stew':{    
        "Name":"Beef Stew",
        "Short Description":  """A hearty and comforting beef stew made with tender beef, potatoes, carrots, and onions in a rich broth.""",
            'Full Description':"Beef stew is a classic comfort food that has been enjoyed for centuries. This recipe uses beef chuck, which becomes incredibly tender after slow cooking, combined with potatoes, carrots, and onions in a savory broth. It’s perfect for a cold day or any time you want a satisfying meal.",
            'Ingredients':"""
        2 pounds beef chuck, cut into 1-inch cubes

        4 cups beef broth

        4 carrots, sliced

        4 potatoes, diced

        1 large onion, sliced

        3 cloves garlic, minced

        2 tablespoons tomato paste

        2 tablespoons olive oil

        2 teaspoons dried thyme

        1 teaspoon dried rosemary

        Salt and pepper to taste

        2 tablespoons all-purpose flour (optional, for thickening)
        """,
            'How to Cook':"""
        Brown the Beef: Heat olive oil in a large pot over medium heat. Add the beef cubes and brown on all sides. Remove the beef and set aside.

        Sauté Vegetables: In the same pot, add the onions, garlic, carrots, and potatoes. Sauté until the onions are translucent.

        Add Broth and Spices: Pour in the beef broth, add tomato paste, thyme, rosemary, and salt and pepper. Stir well to combine.

        Simmer: Return the beef to the pot, bring to a boil, then reduce heat to low. Cover and simmer for 2-3 hours, or until the beef and vegetables are tender.

        Thicken (Optional): If you prefer a thicker stew, mix flour with a little water to create a slurry and stir it into the stew. Let it simmer for another 10 minutes.

        Serve: Serve hot, garnished with fresh parsley if desired.
        """,
            'Facts':
        ["""
        Beef stew has been a staple in many cultures, including Irish, French, and American.    
        ""","""
        The slow cooking process tenderizes the meat and allows the flavors to meld together.
        ""","""
        In Ireland, a similar dish called "Irish stew" traditionally includes lamb or mutton instead of beef.
        """]},
    'Gazpacho':{"Name":"Gazpacho",
        "Short Description":  """A refreshing Spanish cold soup made with tomatoes, cucumbers, bell peppers, and a splash of vinegar.""",
            'Full Description':"Gazpacho is a traditional Spanish cold soup that is perfect for hot summer days. This recipe uses fresh tomatoes, cucumbers, bell peppers, and a hint of vinegar and olive oil to create a refreshing and healthy dish. It’s easy to make and can be customized with your favorite vegetables.",
            'Ingredients':"""
        4 large tomatoes, chopped

        2 cucumbers, chopped

        1 bell pepper, chopped

        1/2 onion, chopped

        1/4 cup red wine vinegar

        1/4 cup olive oil

        1 clove garlic, minced

        1 teaspoon salt

        1/2 teaspoon black pepper

        1/2 cup water or tomato juice (optional)

        Ice cubes (optional, for serving)
        """,
            'How to Cook':"""
        Blend: In a blender or food processor, combine all the ingredients except for the ice cubes. Blend until smooth.

        Chill: Pour the gazpacho into a bowl and refrigerate for at least 1 hour to chill.

        Serve: Serve cold, garnished with chopped cucumber, tomato, or bell pepper. Add ice cubes if desired.
        """,
            'Facts':["Gazpacho originated in the southern Spanish region of Andalusia.",
                    "It was traditionally made by peasants who needed a refreshing meal during hot summers.",
                    "Gazpacho is often served with a variety of toppings, such as chopped onions, bread, or even a drizzle of olive oil."]
                    
        },
    'Chocolate_Lava_Cake':{"Name":"Chocolate Lava Cake",
        "Short Description":  """A rich and decadent chocolate cake with a molten center, served warm with a scoop of vanilla ice cream.""",
            'Full Description':"Chocolate lava cake is a luxurious dessert that is sure to impress. This recipe creates small, individual cakes that are baked just until the edges are set, leaving a gooey, chocolatey center. Serve them warm with a scoop of vanilla ice cream for the perfect contrast.",
            'Ingredients':"""
        1/2 cup unsalted butter

        6 ounces dark chocolate, chopped

        1/2 cup granulated sugar

        1/2 cup all-purpose flour

        3 large eggs

        1 tablespoon cocoa powder

        1/2 teaspoon vanilla extract

        Pinch of salt

        Vanilla ice cream for serving
        """,
            'How to Cook':"""
        Preheat: Preheat the oven to 425°F (220°C). Grease six small ramekins or muffin cups.

        Melt Chocolate and Butter: In a microwave-safe bowl, melt the butter and chocolate together in 30-second intervals, stirring between each interval until smooth.

        Mix Wet Ingredients: In a separate bowl, whisk together the eggs, sugar, vanilla extract, and salt until well combined.

        Combine: Pour the melted chocolate mixture into the egg mixture and whisk until smooth. Add the cocoa powder and flour, and mix until just combined.

        Bake: Pour the batter into the prepared ramekins, filling each about 3/4 full. Bake for 12-15 minutes, or until the edges are set but the center is still slightly jiggly.

        Serve: Let the cakes cool for a few minutes, then carefully run a knife around the edge to loosen. Invert onto a plate and serve immediately with a scoop of vanilla ice cream.
        """,
            'Facts':["Lava cake was popularized in the 1990s, but its origins can be traced back to European molten chocolate cakes.",
                    "The dish is often served with a variety of toppings, such as fresh berries, powdered sugar, or a drizzle of caramel sauce.",
                    "The key to a perfect lava cake is to not overbake it—keep an eye on it and remove it from the oven when the center is still molten."]}
}

# Prompt template for recipe recommendation
prompt_template_recommend = PromptTemplate(
    input_variables=["user_request", "recipe_names"],
    template="""
    You are a helpful assistant that recommends recipe names based on user requests. Here is a list of available recipe names:
    {recipe_names}
    Based on what you know, return one of these recipe names exactly as it is. If the user's request does not match any of these recipe names, return 'None'.
    User Request: {user_request}
    """
)
llm_chain_recommend = LLMChain(llm=llm, prompt=prompt_template_recommend)

# Prompt template for determining what to display
prompt_template_display = """
You are a helpful assistant that responds with what the user is looking for from the available choices: {content}
If the user's request doesn't match any of these, respond with 'None'.

Here's the recipe we're talking about:
{to_send}

User Request: {user_request}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    recommended_recipe = None
    if request.method == 'POST':
        user_request = request.form['request']
        recipe_names = ', '.join(recipes.keys())
        response = llm_chain_recommend.run(user_request=user_request, recipe_names=recipe_names)
        recommended_recipe = response.strip()
        if recommended_recipe in recipes:
            return redirect(url_for('recipe', recipe_name=recommended_recipe))
        else:
            return redirect(url_for('no_recipe'))
    return render_template('index.html')

@app.route('/recipe/<recipe_name>', methods=['GET', 'POST'])
def recipe(recipe_name):
    if recipe_name not in recipes:
        return redirect(url_for('no_recipe'))
    recipe_data = recipes[recipe_name]
    if request.method == 'POST':
        user_request = request.form['request']
        content_list = ['Name', 'Short Description', 'Full Description', 'Ingredients', 'How to Cook', 'Facts']
        prompt = prompt_template_display.format(content=content_list, to_send=f"Dish name: {recipe_data['Name']}, Dish short description: {recipe_data['Short Description']}", user_request=user_request)
        message = llm.invoke(prompt)
        response = message.content.strip()
        if response in content_list:
            if response == 'Facts':
                fact = random.choice(recipe_data['Facts'])
                return render_template('recipe.html', recipe=recipe_data, fact=fact)
            else:
                return render_template('recipe.html', recipe=recipe_data, content=recipe_data.get(response, ''))
        else:
            return render_template('recipe.html', recipe=recipe_data, error='Sorry, your request could not be fulfilled.')
    return render_template('recipe.html', recipe=recipe_data)

@app.route('/no_recipe')
def no_recipe():
    return render_template('no_recipe.html')

if __name__ == '__main__':
    app.run(debug=True)