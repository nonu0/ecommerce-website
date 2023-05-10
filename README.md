# ecommerce-website

# Django E-commerce Website

This is a Django-based e-commerce website that allows users to view products, add them to a shopping cart, and proceed to checkout. It includes various views and templates to handle different functionalities of the website.

## Features

- Home Page: Displays a landing page with information about the website.
- Cart: Allows users to view their shopping cart, update quantities, and remove items.
- Shop: Displays a list of products available for purchase. Supports pagination for easy navigation.
- Product Detail: Shows detailed information about a specific product.
- Add to Cart: Enables users to add products to their shopping cart.
- Checkout: Provides a form for users to enter their details and complete the purchase.
- Profile: Shows the user's profile page with their order history.
- Contact: Displays a contact page for users to get in touch.
- Blog: Shows a blog page with relevant articles.
- Services: Provides information about the services offered by the website.
- About: Provides information about the website and its mission.

## Dependencies

This project requires the following dependencies:

- Django (version 4.2.0): A high-level Python web framework.
- Python (version 3.1.1): The programming language used for development.
- Other dependencies: Make sure to install all the required packages mentioned in the `requirements.txt` file.

## Installation and Setup

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo.git
```

2. Navigate to the project directory:

```
cd project-directory
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Run the migrations:

```
python manage.py migrate
```

5. Start the development server:

```
python manage.py runserver
```

6. Open your web browser and visit `http://localhost:8000` to access the website.

## Configuration

- Database: By default, this project uses the SQLite database. If you want to use a different database, update the database settings in the `settings.py` file.

- Static files: The project includes static files such as CSS, JavaScript, and images. Make sure to configure the static file settings in the `settings.py` file to serve these files correctly.

- Email settings: If you want to enable email functionality, update the email settings in the `settings.py` file to use your SMTP server credentials.

## Usage

- Visit the home page to get an overview of the website and its features.
- Browse the shop to view available products and their details.
- Click on a product to view its detailed information.
- Add products to your shopping cart by clicking the "Add to Cart" button.
- View your cart to see the added products, update quantities, or remove items.
- Proceed to the checkout page to enter your details and complete the purchase.
- If you are a registered user, you can view your profile page with order history.
- Contact the website administrators through the contact page for any queries or issues.
- Explore the blog page for relevant articles and information.
- Learn about the services provided by the website on the services page.
- Get more information about the website and its mission on the about page.

## Contribution

Contributions to this project are welcome. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute it as per the license terms.
