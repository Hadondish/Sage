# Sage
Nutrition analyzer to take nutritional labels and final labels.

## Development

### Database

Sage uses a SQLite3 database, located in the `data` directory.

To add items to the DB, upload an image to the directory. Update `food_info.sql` with the image name, item name, and price.

To update the database after adding a new item:

```zsh
cd data
sqlite3 food_info.db < food_info.sql
```