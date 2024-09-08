import csv

# Function to handle SKU processing with image fix
def process_sku_data_with_image_fix(sku_file_path, product_file_path, output_file_path):
    transformed_variants = []

    # Read the product file into a list for easier lookup
    product_images = []
    with open(product_file_path, mode='r', encoding='utf-8') as product_file:
        product_reader = csv.DictReader(product_file)
        for product_row in product_reader:
            product_images.append(product_row)

    # Read the SKU file and process it
    with open(sku_file_path, mode='r', encoding='utf-8') as sku_file:
        sku_reader = csv.DictReader(sku_file)

        for sku_row in sku_reader:
            # Extract attribute names and values
            attr_names = sku_row['Attribute Names (Name:Type:Position)'].split('|')
            attr_values = sku_row['Attribute Values (Value:Position)'].split('|')

            # Prepare the variant row
            variant_row = {
                'id': sku_row['Product ID'],
                'Option1 Name': attr_names[0] if len(attr_names) > 0 else '',
                'Option1 Value': attr_values[0] if len(attr_values) > 0 else '',
                'Option2 Name': attr_names[1] if len(attr_names) > 1 else '',
                'Option2 Value': attr_values[1] if len(attr_values) > 1 else '',
                'Option3 Name': attr_names[2] if len(attr_names) > 2 else '',
                'Option3 Value': attr_values[2] if len(attr_values) > 2 else '',
                'Variant Price': sku_row['Impact on Price'],
                'Variant Compare At Price': sku_row['Wholesale Price'],
                'Variant Qty': sku_row['Quantity'],
                'Variant Image': ''  # This will be handled below
            }

            # Handle image logic
            if sku_row['Images (x,y,z…)']:
                image_urls = sku_row['Images (x,y,z…)'].split('|')
                for image_url in image_urls:
                    if image_url.endswith('.jpg'):
                        # Extract product code from the URL
                        product_code = image_url.split('/')[-2]
                        # Search for a matching product image
                        for product_row in product_images:
                            if product_code in product_row['Image Src']:
                                variant_row['Variant Image'] = product_row['Image Src']
                                break
                    else:
                        # If valid image, directly assign
                        variant_row['Variant Image'] = image_url

            transformed_variants.append(variant_row)

    # Write the transformed variant data to a new CSV file
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as output_file:
        fieldnames = ['id', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant Price', 'Variant Compare At Price', 'Variant Qty', 'Variant Image']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the transformed rows
        for variant in transformed_variants:
            writer.writerow(variant)

# Example usage
sku_file_path = 'sku_data.csv'
product_file_path = 'product_data.csv'
output_file_path = 'output_variants.csv'

# Call the function to process and write the data
process_sku_data_with_image_fix(sku_file_path, product_file_path, output_file_path)
