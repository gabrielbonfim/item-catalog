# Catalog App
Application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users have the ability to post, edit and delete their own items. The application also provides JSON endpoints to access information about the catalog.

## [Project Files](https://github.com/gabrielbonfim/item-catalog)
- `application.py` - Catalog application
- `client_secrets.json` - JSON file containing the client ID, client secret, and other OAuth 2.0 parameters
- `create_default_categories_and_items.py` - Creation of categories and items (optional execution)
- `database_setup.py` - Mapper file for database and tables creation
- `static\styles.css` - Application CSS
- `static\default.png` - Default item image when none is defined by the user
- `static\home.png` - Home hyperlink image
- `static\README_img1.png` - README image - Application description
- `static\README_img2.png` - README image - Application description
- `static\README_img3.png` - README image - Application description
- `static\README_img4.png` - README image - Application description
- `static\README_img5.png` - README image - Application description
- `static\README_img6.png` - README image - Application description
- `static\README_img7.png` - README image - Application description
- `templates\category_add.html` - Layout for the creation of a new category
- `templates\category_items.html` - Layout for the items of a given category
- `templates\delete_confirm.html` - Layout for the confirmation of categories and items delete action
- `templates\item_add.html` - Layout for the creation of a new item
- `templates\item_detail.html` - Layout for the item details
- `templates\latest_items.html` - Layout for the latest 10 items added
- `templates\layout.html` - Base layout with the header and footer
- `templates\login.html` - Login layout
- `templates\logout.html` - Logout layout
- `LICENSE` - The license associated with this project
- `README.md` - This file

## Getting Started
### Prerequisites
- Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads). You do not need to launch VirtualBox after installing it.
- Install [Vagrant](https://www.vagrantup.com/downloads.html). Vagrant is the program that will download a Linux operating system and run it inside the virtual machine.
- Clone the [VM configuration](https://github.com/gabrielbonfim/fullstack-nanodegree-vm). `cd` into the "vagrant" directory and execute `vagrant up`. This will copy (in the first run) and start the virtual machine. Once started access the virtual machine via SSH with `vagrant ssh` (password is vagrant).
- Move to catalog folder with `cd /vagrant/catalog`
- [Python](https://www.python.org/) - Already installed in the virtual machine
- [Flask](http://flask.pocoo.org/) - Already installed in the virtual machine
- [SQLAlchemy](https://www.sqlalchemy.org/) - Already installed in the virtual machine

### Installing
```
git clone https://github.com/gabrielbonfim/item-catalog
```

### Usage
```
cd item-catalog
python database_setup.py
python create_default_categories_and_items.py (optional)
python application.py
```

Access the application in the browser:
[http://localhost:8000](http://localhost:8000)

### Application description
- Main layout with no user authenticated

![image1](/static/README_img1.png)

- Login

![image2](/static/README_img2.png)

- Main layout with authenticated user

![image3](/static/README_img3.png)

- New category creation

![image4](/static/README_img4.png)

- New item creation. This layout is fulfilled by the item details when we edit a item

![image5](/static/README_img5.png)

- Item detail

![image6](/static/README_img6.png)

- Confirmation of deletion of items and categories

![image7](/static/README_img7.png)

### JSON Endpoints
- [http://localhost:8000/api/v1.0/catalog](http://localhost:8000/api/v1.0/catalog) - Returns all the categories and its items
- [http://localhost:8000/api/v1.0/category/all](http://localhost:8000/api/v1.0/category/all) - Returns all the categories
- [http://localhost:8000/api/v1.0/category/<category_id>/items](http://localhost:8000/api/v1.0/category/<category_id>/items) - Returns all the items in a specific category
- [http://localhost:8000/api/v1.0/item/<item_id>](http://localhost:8000/api/v1.0/item/<item_id>) - Returns the detail of an item

### Enjoy
&#128526;

## Build With
[Visual Studio Code](https://code.visualstudio.com/)

## Author
[Gabriel Almeida](https://www.linkedin.com/in/gabriel-bonfim-almeida/) (Udacity Student)

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/gabrielbonfim/item-catalog/blob/master/LICENSE) file for details