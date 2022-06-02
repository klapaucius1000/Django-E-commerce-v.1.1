The first major update to my project, an e-commerce shop for insectivorous plants. 
Link to version 1.0 here: https://github.com/PapaBear928/Django-E-commerce

. There have been a few noteworthy changes to the project:

What's new?
- Remodelled database according to the MPTT system
- The ability to add shipping addresses created in accordance with CRUD.
- Also added the ability to create a list of favorite products from the shop. 
- Added REST, and documentation created with Swagger
- Other minor code changes

What else will be here?

- Adding the BLOG module
- Adding missing or empty pages (e.g. stationary shops)
- Integration with PayPal
- Tests
- Deploing at Heroku or something
- Something else I'll probably come up with.
 

<h2>Used tech:</h2>
<h4>Python 3.10.2</h4>
<h4> HTML5</h4>
<h4> CSS</h4>
<h4> AJAX</h4>
<h4> STRIPE</h4>

<br><br><br>


<h2>SETUP(as if someone didn't know that):</h2>


To run setup first create virtual environment<br>
  <i>py -m venv venv</i>


Then, after your venv folder is created open it by<br>
  <i>venv\scripts\activate</i>


And then install requirements included in filde requirements.txt<br>
  <i>pip install -r requirements.txt</i>


After instalation complete you can run server with project<br>
  <i>py manage.py runserver</i>
  
  

 <b>This app have email verification system, so be attention to use existing email adress.</b>


<h2> Features</h2>

The main feature of this project was creating an online store, which will include all features that the real shop has.

<h4>Home</h4>

In home screen I've decided to put little greeting. If the user is logged in, there will be a button to go to the store. If not, the button will redirect him to the login page.He can also click on the navbar, where there are links to the store, not yet implemented website functions and to the user panel and login.

<h4>Our products</h4>

Under the name "Our products" there is a store divided according to categories assigned by the administrator who places the product in the store.<b>Added ability to add products to Wish lists and save for later.</b>

<h4>Account</h4>

In the "account" panel, the user can change his basic data.<b>The user can add delivery addresses themselves. At the same time, the possibility of setting one of them as the default delivery address has been added.There is also an icon which refers the user to their Wish list. If nothing has been selected, the user will read an appropriate message about the lack of favourite products.</b>

<h4>Login</h4>

In the "Login" panel, the user can recover his password, register or log in to the website.

<h4>Shopping Cart</h4>

If the user is logged in,he has acces to his shopping cart. If the cart is empty, the user will only find a link to the store there. If there are any items in the basket, the user will add up the information about the total cost of the order, including shipping. From the same panel it is possible to change the number of ordered products or to delete the order. After clicking "Checkout" we will be taken to the payment finalization.

<h4>Payment</h4>

After completing the data, STRIPE will guide you through the payment process.
