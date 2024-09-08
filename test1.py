import csv


# Function to handle collection trimming and transformation
def transform_data_with_collection_fix(product_file_path,sku_file_path, output_file_path):
    transformed_rows = []
    product_images = []
    with open(product_file_path, mode='r', encoding='utf-8') as product_file:
        product_reader = csv.DictReader(product_file)
        for product_row in product_reader:
            image_urls = product_row['Image URLs (x,y,z...)'].split('|')
            product_images.extend(image_urls)
    print(len(product_images))
    sku_file=open(sku_file_path, mode='r', encoding='utf-8')
    sku_reader = list(csv.DictReader(sku_file))
    sku_index=0
    # Open and read the CSV file
    with open(product_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Iterate through each row of the input CSV file
        for row in reader:
            # Extract only the last part of the collection (after the last "=>")
            if row['Categories (x,y,z...)']:
                collections = row['Categories (x,y,z...)'].split('|')
                last_collections = [col.split('=>')[-1] for col in collections]
                collection_str = ','.join(last_collections)
            else:
                collection_str = ''

            # Base row with most fields transformed
            base_row = {
                'id': row['Product ID'],
                'Handle': row['Friendly URL EN'],
                'Spu': row['Product ID'],  # Assuming 'Spu' is the same as 'Product ID'
                'Title': row['Name EN'],
                'Sub Title': '',  # No source data for this field
                'Body（Html）': row['Long Description EN'],
                'Collection': collection_str,
                'Meta Title': row['Meta Title EN'],
                'Meta Keywords': '',  # No source data for this field
                'Meta Description': row['Meta Description EN'],
                'Status': '1' if row['Active (0=No, 1=Yes)'] == '1' else '2',
                'Virtual Sales Count': '0',
                'Variant Type': '2',  # Default to 1 (single variant)
                'Vendor': row['Manufacturer'],
                'Sale Count': '0',
                'Inventory Police': '2',  # Default to 2
                'Inventory Police Type': '1',  # Default to 1
                'Remote Id': '',  # No source data for this field
                'Variant Price': row['Price Tax Inc'],
                'Variant Compare At Price': '',  # No source data for this field
                'Variant Cost Price': '',  # No source data for this field
                'Variant SKU': row['MPN'],
                'Variant Grams': '',  # No source data for this field
                'Variant Barcode': '',  # No source data for this field
                'Variant Qty': '',  # No source data for this field
                'Variant Weight': '',  # No source data for this field
                'Variant Weight Unit': 'g',  # Default to grams
                'Variant Note': '',  # No source data for this field
                'Option1 Name':  '',
                'Option1 Value':'',
                'Option2 Name':  '',
                'Option2 Value':  '',
                'Option3 Name': '',
                'Option3 Value':  '',
                'Variant Image': ''  # This will be handled below
            }

            # Handle the image URLs if they exist
            if row['Image URLs (x,y,z...)']:
                image_urls = row['Image URLs (x,y,z...)'].split('|')
                for idx, image_url in enumerate(image_urls):
                    print('产品id:',row['Product ID'])
                    print('sku ID:',sku_reader[sku_index]['Product ID'])
                    print('SKU index',sku_index)
                    if(sku_index>=len(sku_reader)-1):
                        sku_index=len(sku_reader)-3
                        sku_reader[sku_index]['Product ID']=99999
                    if idx == 0:
                        if (sku_reader[sku_index]['Product ID'] == row['Product ID']):
                            attr_names = sku_reader[sku_index]['Attribute Names (Name:Type:Position)'].split('|')
                            attr_values = sku_reader[sku_index]['Attribute Values (Value:Position)'].split('|')

                            # For the first image, add the image data to the base row
                            base_row['Image Src'] = image_url
                            base_row['Image Position'] = '1'
                            base_row['Image Alt Text'] = row['Name EN']
                            base_row['Option1 Name']= attr_names[0] if len(attr_names) > 0 else ''
                            base_row['Option1 Value']=attr_values[0] if len(attr_values) > 0 else ''
                            base_row['Option2 Name']=attr_names[1] if len(attr_names) > 1 else ''
                            base_row['Option2 Value']= attr_values[1] if len(attr_values) > 1 else ''
                            base_row['Option3 Name']= attr_names[2] if len(attr_names) > 2 else ''
                            base_row['Option3 Value']= attr_values[2] if len(attr_values) > 2 else ''
                            base_row['Variant Price']= sku_reader[sku_index]['Impact on Price']
                            base_row['Variant Compare At Price']= sku_reader[sku_index]['Wholesale Price']
                            base_row['Variant Qty']= sku_reader[sku_index]['Quantity']
                            base_row['Variant Image']= ''  # This will be handled below
                            if sku_reader[sku_index]['Images (x,y,z…)']:
                                image_urls = sku_reader[sku_index]['Images (x,y,z…)'].split('|')
                                image_url=image_urls[0]
                                if image_url.endswith('.jpg'):
                                    # Extract product code from the URL
                                    product_code = image_url.split('/')[-2]
                                    print(product_code)
                                    # Search for a matching product image
                                    for images in product_images:
                                        if product_code in images:
                                            base_row['Variant Image'] = images
                                            print(images)
                                            break
                            sku_index += 1
                        transformed_rows.append(base_row)
                    else:
                        # For subsequent images, create new rows with only image data
                        if (sku_reader[sku_index]['Product ID'] == row['Product ID']):
                            attr_names = sku_reader[sku_index]['Attribute Names (Name:Type:Position)'].split('|')
                            attr_values = sku_reader[sku_index]['Attribute Values (Value:Position)'].split('|')
                            image_row = {
                                'id': row['Product ID'],
                                'Handle': row['Friendly URL EN'],
                                'Image Src': image_url,
                                'Image Position': str(idx + 1),
                                'Image Alt Text': row['Name EN'],
                                'Option1 Name': attr_names[0] if len(attr_names) > 0 else '',
                                'Option1 Value': attr_values[0] if len(attr_values) > 0 else '',
                                'Option2 Name': attr_names[1] if len(attr_names) > 1 else '',
                                'Option2 Value': attr_values[1] if len(attr_values) > 1 else '',
                                'Option3 Name': attr_names[2] if len(attr_names) > 2 else '',
                                'Option3 Value': attr_values[2] if len(attr_values) > 2 else '',
                                'Variant Price': sku_reader[sku_index]['Impact on Price'],
                                'Variant Compare At Price': sku_reader[sku_index]['Wholesale Price'],
                                'Variant Qty': sku_reader[sku_index]['Quantity'],
                                'Variant Image': ''  # This will be handled below
                            }
                            if sku_reader[sku_index]['Images (x,y,z…)']:
                                image_urls = sku_reader[sku_index]['Images (x,y,z…)'].split('|')
                                image_url=image_urls[0]
                                if image_url.endswith('.jpg'):
                                    # Extract product code from the URL
                                    product_code = image_url.split('/')[-2]
                                    print(product_code)
                                    # Search for a matching product image
                                    for product_row in product_images:
                                        if product_code in product_row:
                                            image_row['Variant Image'] = product_row
                                            print(product_row)
                                            break
                            sku_index += 1
                        else:
                            image_row = {
                                'id': row['Product ID'],
                                'Handle': row['Friendly URL EN'],
                                'Image Src': image_url,
                                'Image Position': str(idx + 1),
                                'Image Alt Text': row['Name EN'],
                            }
                        transformed_rows.append(image_row)

                #处理sku超过图片的情况
                while(sku_reader[sku_index]['Product ID'] == row['Product ID']):
                    attr_names = sku_reader[sku_index]['Attribute Names (Name:Type:Position)'].split('|')
                    attr_values = sku_reader[sku_index]['Attribute Values (Value:Position)'].split('|')
                    image_row = {
                        'id': row['Product ID'],
                        'Handle': row['Friendly URL EN'],
                        'Option1 Name': attr_names[0] if len(attr_names) > 0 else '',
                        'Option1 Value': attr_values[0] if len(attr_values) > 0 else '',
                        'Option2 Name': attr_names[1] if len(attr_names) > 1 else '',
                        'Option2 Value': attr_values[1] if len(attr_values) > 1 else '',
                        'Option3 Name': attr_names[2] if len(attr_names) > 2 else '',
                        'Option3 Value': attr_values[2] if len(attr_values) > 2 else '',
                        'Variant Price': sku_reader[sku_index]['Impact on Price'],
                        'Variant Compare At Price': sku_reader[sku_index]['Wholesale Price'],
                        'Variant Qty': sku_reader[sku_index]['Quantity'],
                        'Variant Image': ''  # This will be handled below
                    }
                    if sku_reader[sku_index]['Images (x,y,z…)']:
                        image_urls = sku_reader[sku_index]['Images (x,y,z…)'].split('|')
                        image_url=image_urls[0]
                        if image_url.endswith('.jpg'):
                            # Extract product code from the URL
                            product_code = image_url.split('/')[-2]
                            # Search for a matching product image
                            for product_row in product_images:
                                if product_code in product_row:
                                    image_row['Variant Image'] = product_row
                                    break
                    sku_index += 1
                    transformed_rows.append(image_row)
            else:
                # If there are no images, append the base row without image data
                transformed_rows.append(base_row)

    # Write the transformed data to a new CSV file
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['id', 'Handle', 'Spu', 'Title', 'Sub Title', 'Body（Html）', 'Collection', 'Meta Title',
                      'Meta Keywords', 'Meta Description', 'Status', 'Virtual Sales Count', 'Variant Type', 'Vendor',
                      'Sale Count', 'Inventory Police', 'Inventory Police Type', 'Remote Id', 'Image Src',
                      'Image Position',
                      'Image Alt Text', 'Variant Price', 'Variant Compare At Price', 'Variant Cost Price',
                      'Variant SKU',
                      'Variant Grams', 'Variant Barcode', 'Variant Qty', 'Variant Image', 'Option1 Name',
                      'Option1 Value',
                      'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant Weight',
                      'Variant Weight Unit',
                      'Variant Note']

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Writing the header
        writer.writeheader()

        # Defining the second row with missing columns filled as ''
        secondrow = {
            'id': '产品id',
            'Handle': '产品Url Handle',
            'Spu': 'Spu',
            'Title': '产品标题',
            'Sub Title': '产品副标题',
            'Body（Html）': '产品描述',
            'Collection': '产品专辑，多个专辑用英文逗号隔开',
            'Meta Title': 'Meta Title',
            'Meta Keywords': 'Meta Keywords',
            'Meta Description': 'Meta Description',
            'Status': '产品状态，1代表上架，2代表下架',
            'Virtual Sales Count': '产品虚拟销量',
            'Variant Type': '产品类型，1为单规格，2为多规格',
            'Vendor': '产品供应商的名称',
            'Sale Count': '产品实际销量',
            'Inventory Police': '是否跟踪库存，1为跟踪，2为不跟踪',
            'Inventory Police Type': '跟踪库存时有效：1为库存为0，允许购买，2为库存为0不允许购买，3库存为0自动下架',
            'Remote Id': '远程id，一般作为同步数据使用',
            'Image Src': '产品图片Src Url',
            'Image Position': '产品图片排序位置',
            'Image Alt Text': '图片Alt',
            'Variant Price': '变体(规格)价格',
            'Variant Compare At Price': '变体划线价格（原价）',
            'Variant Cost Price': '变体成本价格',
            'Variant SKU': '变体sku',
            'Variant Grams': '重量：克',
            'Variant Barcode': '产品的条形码、UPC 或 ISBN 号。',
            'Variant Qty': '变体库存个数',
            'Variant Image': '变体图片',
            'Option1 Name': '变体规格属性1-名称',
            'Option1 Value': '变体规格属性1-值',
            'Option2 Name': '变体规格属性2-名称',
            'Option2 Value': '变体规格属性2-值',
            'Option3 Name': '变体规格属性3-名称',
            'Option3 Value': '变体规格属性3-值',
            'Variant Weight': '变体重量',
            'Variant Weight Unit': '重量单位（kg 或者 g），kg为千克，g为克',
            'Variant Note': '变体备注'
        }

        # Filling missing columns with empty strings
        for field in fieldnames:
            if field not in secondrow:
                secondrow[field] = ''

        # Writing the second row
        writer.writerow(secondrow)
        # Write the transformed rows
        for row in transformed_rows:
            writer.writerow(row)


# Example usage
product_file_path = 'export_08-09-2024_200724 (2).csv'
sku_file_path='export_08-09-2024_201304.csv'
output_file_path = 'output_file1.csv'

# Call the function to transform and write the data
transform_data_with_collection_fix(product_file_path, sku_file_path,output_file_path)
