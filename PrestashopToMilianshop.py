import pandas as pd

# Function to process product data
def transform_product_data(product_file_path):
    # Load product data
    product_df = pd.read_csv(product_file_path)

    # Handle collection and product-related transformations
    def transform_data_with_collection_fix(input_df):
        transformed_rows = []

        for _, row in input_df.iterrows():
            if pd.notna(row['Categories (x,y,z...)']):
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
                'Status': 1 if row['Active (0=No, 1=Yes)'] == 1 else 2,
                'Variant Type': 1,  # Default to 1
                'Vendor': row['Manufacturer'],
                'Variant Price': row['Price Tax Inc'],
                'Variant SKU': row['MPN'],
                'Image Src': row['Cover Image URL'],  # Default image handling
            }

            # If there are no images, append the base row without image data
            transformed_rows.append(base_row)

        return pd.DataFrame(transformed_rows)

    return transform_data_with_collection_fix(product_df)

# Function to process SKU/variant data and merge with product data
def process_sku_data(sku_file_path, product_df):
    sku_df = pd.read_csv(sku_file_path)

    def process_sku_data_with_image_fix(sku_df, product_df):
        transformed_variants = []

        for _, sku_row in sku_df.iterrows():
            attr_names = str(sku_row['Attribute Names (Name:Type:Position)']).split('|')
            attr_values = str(sku_row['Attribute Values (Value:Position)']).split('|')

            variant_row = {
                'id': sku_row['Product ID'],
                'Option1 Name': attr_names[0] if len(attr_names) > 0 else '',
                'Option1 Value': attr_values[0] if len(attr_values) > 0 else '',
                'Option2 Name': attr_names[1] if len(attr_names) > 1 else '',
                'Option2 Value': attr_values[1] if len(attr_values) > 1 else '',
                'Variant Price': sku_row['Impact on Price'],
                'Variant Compare At Price': sku_row['Wholesale Price'],
                'Variant Qty': sku_row['Quantity'],
                'Variant Image': '',
            }

            if pd.notna(sku_row['Images (x,y,z…)']):
                image_urls = str(sku_row['Images (x,y,z…)']).split('|')
                for image_url in image_urls:
                    if image_url.endswith('.jpg'):
                        product_code = image_url.split('/')[-2]
                        matching_image = product_df[product_df['Image Src'].str.contains(product_code, na=False)]
                        if not matching_image.empty:
                            variant_row['Variant Image'] = matching_image.iloc[0]['Image Src']
                            break
                    else:
                        variant_row['Variant Image'] = image_url

            transformed_variants.append(variant_row)

        return pd.DataFrame(transformed_variants)

    return process_sku_data_with_image_fix(sku_df, product_df)

# Main function to merge the data and output the final file
def merge_and_output(product_file_path, sku_file_path, output_file_path):
    # Step 1: Process the product file
    product_df = transform_product_data(product_file_path)

    # Step 2: Process the SKU/variant file and merge with product data
    transformed_sku_df = process_sku_data(sku_file_path, product_df)

    # Step 3: Combine product and variant data (handling potential mismatches)
    final_df = pd.merge(product_df, transformed_sku_df, on='id', how='left')

    # Output the final CSV file
    final_df.to_csv(output_file_path, index=False)
    print(f"Final file saved to {output_file_path}")

# Example usage
if __name__ == "__main__":
    # File paths for user input
    product_file = input("Enter the path to the product file: ")
    sku_file = input("Enter the path to the SKU file: ")
    output_file = input("Enter the path for the output file: ")

    # Merge the files and produce the output
    merge_and_output(product_file, sku_file, output_file)
