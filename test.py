import csv


# Function to process product data
def transform_product_data(product_file_path):
    transformed_rows = []

    with open(product_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Handle categories and collections
            if row['Categories (x,y,z...)']:
                collections = row['Categories (x,y,z...)'].split('|')
                last_collections = [col.split('=>')[-1] for col in collections]
                collection_str = ','.join(last_collections)
            else:
                collection_str = ''

            base_row = {
                'id': row['Product ID'],
                'Handle': row['Friendly URL EN'],
                'Spu': row['Product ID'],
                'Title': row['Name EN'],
                'Body（Html）': row['Long Description EN'],
                'Collection': collection_str,
                'Meta Title': row['Meta Title EN'],
                'Meta Description': row['Meta Description EN'],
                'Status': '1' if row['Active (0=No, 1=Yes)'] == '1' else '2',
                'Variant Type': '1',  # Default to 1
                'Vendor': row['Manufacturer'],
                'Variant Price': row['Price Tax Inc'],
                'Variant SKU': row['MPN'],
                'Image Src': row['Cover Image URL'],  # Default image handling
            }

            # Append base row data
            transformed_rows.append(base_row)

    return transformed_rows


# Function to process SKU/variant data and merge with product data
def process_sku_data(sku_file_path, product_rows):
    transformed_variants = []

    with open(sku_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for sku_row in reader:
            attr_names = sku_row['Attribute Names (Name:Type:Position)'].split('|')
            attr_values = sku_row['Attribute Values (Value:Position)'].split('|')

            variant_row = {
                'id': sku_row['Product ID'],
                'Option1 Name': attr_names[0] if len(attr_names) > 0 else '',
                'Option1 Value': attr_values[0] if len(attr_values) > 0 else '',
                'Option2 Name': attr_names[1] if len(attr_names) > 1 else '',
                'Option2 Value': attr_values[1] if len(attr_values) > 1 else '',
                'Variant Price': sku_row['Impact on Price'],
                'Variant Compare At Price': sku_row['Wholesale Price'],
                'Variant Qty': sku_row['Quantity'],
                'Variant Image': ''
            }

            # Process image URLs for SKU
            if sku_row['Images (x,y,z…)']:
                image_urls = sku_row['Images (x,y,z…)'].split('|')
                for image_url in image_urls:
                    if image_url.endswith('.jpg'):
                        product_code = image_url.split('/')[-2]
                        for product_row in product_rows:
                            if product_code in product_row['Image Src']:
                                variant_row['Variant Image'] = product_row['Image Src']
                                break
                    else:
                        variant_row['Variant Image'] = image_url

            transformed_variants.append(variant_row)

    return transformed_variants


# Main function to merge the data and output the final file
def merge_and_output(product_file_path, sku_file_path, output_file_path):
    # Step 1: Process the product file
    product_rows = transform_product_data(product_file_path)

    # Step 2: Process the SKU/variant file
    transformed_sku_rows = process_sku_data(sku_file_path, product_rows)

    # Step 3: Combine product and variant data
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as output_file:
        fieldnames = ['id', 'Handle', 'Spu', 'Title', 'Body（Html）', 'Collection', 'Meta Title', 'Meta Description',
                      'Status', 'Variant Type', 'Vendor', 'Variant Price', 'Variant SKU', 'Image Src', 'Option1 Name',
                      'Option1 Value', 'Option2 Name', 'Option2 Value', 'Variant Compare At Price', 'Variant Qty',
                      'Variant Image']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()

        # Write product rows
        for row in product_rows:
            writer.writerow(row)

        # Write SKU variant rows
        for row in transformed_sku_rows:
            writer.writerow(row)

    print(f"Final file saved to {output_file_path}")


# Example usage
if __name__ == "__main__":
    # File paths for user input
    product_file = 'export_08-09-2024_200724 (2).csv'
    sku_file = 'export_08-09-2024_201304.csv'
    output_file = 'output_file.csv'

    # Merge the files and produce the output
    merge_and_output(product_file, sku_file, output_file)
