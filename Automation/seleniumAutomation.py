'''
Created on 16 Jan 2024

@author: yusuf
'''

import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium. common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import json

def test_addingProduct():
    """Test Case 12: Add Products in Cart"""
    f = open ('data.json', "r") 
    # Reading from file
    data = json.loads(f.read())

    #Open LogIn Page
    driver = webdriver.Chrome()
    driver.get(f'{data["mainUrl"]}')

    a = ActionChains(driver)
    
    #Verification of Loading of Home Page
    try:
        WebDriverWait(driver, (4 * data["sleepForWait"])).until(EC.visibility_of_element_located((By.XPATH, f'{data["logoXpath"]}')))
    except TimeoutException as e:
        assert False, f"Verify That Main Page is loaded! : FAILED : {e}"

    print("Verify That Main Page is loaded! : PASSED")

    parent_element = driver.find_element(By.CLASS_NAME, 'features_items')
    products = parent_element.find_elements(By.CLASS_NAME, 'col-sm-4')

    #Verification of products (more than 0) in Home Page
    assert len(products) != 0, f"Verify That all products are loaded successfully : FAILED" 

    print("Verify That all products are loaded successfully : PASSED")

    productsFeatures = []
    index = 1
    for element in products:
        a.move_to_element(element).perform()

        sleep(data["sleepForWait"])
        #Verification Of Overlay 
        try:
            overLayDiv = element.find_element(By.CLASS_NAME, data['overlayClassName'])           
        except Exception as e:
            assert False, f"Verify That Overlay is displayed : FAILED : {e}" 
        print("Verify That Overlay is displayed : PASSED")

        #Verification Off Add cart Button
        try:           
            overLayDiv.find_element(By.TAG_NAME, 'a').click()                   
        except Exception as e:
            assert False, f"Verify That Add cart Button is displayed : FAILED : {e}"   

        print("Verify That Add cart Button is displayed : PASSED")

        #Save Price Of Product
        try:
            name = overLayDiv.find_element(By.TAG_NAME, 'p').get_attribute("innerText")
            price = overLayDiv.find_element(By.TAG_NAME, 'h2').get_attribute("innerText") 
            productsFeatures.append({"name" : name,
                                     "price" :  price})  
        except Exception as e:
            assert False, f"Verify That Product Name and Price are displayed : FAILED : {e}" 
        
        print(f"Verify That Product Name ({name}) and Price ({price}) are displayed : PASSED")

        #Verification Off Added Modal
        try:
            addedModal = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-content')))         
        except Exception as e:
            assert False, f"Verify That Added Model is displayed : FAILED : {e}" 

        print("Verify That Added Model is displayed : PASSED")

        #Verification Of Continue Shopping Button Click Func
        try:
            addedModal.find_element(By.XPATH, "//*[contains(text(), 'Continue Shopping')]").click()      
        except Exception as e:
            assert False, f"Verify That Continue Shopping Button is displayed : FAILED : {e}"  
        
        print("Verify That Continue Shopping Button is displayed : PASSED")

        if index == data['productNumber']:
            break
        index = index + 1

    #Verification of View Cart Button        
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f'{data["viewCartButtonXpath"]}'))).click()       
    except Exception as e:
        assert False, f"Verify That View Cart Button is displayed : FAILED : {e}"  

    print("Verify That View Cart Button is displayed : PASSED")

    #Verification of Product List
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f'{data["productTableXpath"]}')))      
    except Exception as e:
        assert f"Verify That Product List is displayed in Shopping Cart Page : FAILED : {e}"

    print("Verify That Product List is displayed in Shopping Cart Page : PASSED")

    #Verification of products
    parent_element = driver.find_element(By.XPATH, f'{data["productTableXpath"]}')
    products = parent_element.find_elements(By.TAG_NAME, 'tr')
    #head+2 product = 3 tr is verified
    assert len(products) == getProductTypeNumber(productsFeatures) + 1, f"Verify that two product is displayed in Cart, number of Product : {len(products)} : FAILED"

    print(f"Verify that two product is displayed in Cart, number of Product : {len(products) - 1} : PASSED")

    #Verifications of product properties
    for product in productsFeatures:
        #Verify Name
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{product["name"]}')]")))      
        except Exception as e:
            assert f"Verify That Product with name {product["name"]} is displayed in cart: FAILED : {e}"
        #Verify Price  
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{product["price"]}')]")))      
        except Exception as e:
            assert f"Verify That Product with name {product["price"]} is displayed in cart: FAILED : {e}" 
        #Verify Quantity  
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{getProductNumber(product["name"], productsFeatures)}')]")))      
        except Exception as e:
            assert f"Verify That Product with name {product["price"]} is displayed in cart: FAILED : {e}" 
        #Verify Total  
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), 'Rs. {getProductTotal(product["name"], productsFeatures)}')]")))      
        except Exception as e:
            assert f"Verify That Product with name {product["price"]} is displayed in cart: FAILED : {e}" 


        print(f"Verify That Product with name: {product["name"]} is displayed with price: {product["price"]}, quantity : {getProductNumber(product["name"], productsFeatures)}, total : Rs. {getProductTotal(product["name"], productsFeatures)} in cart: PASSED")

def getProductTypeNumber(productFeatureList): 
    '''return number of different product in input List'''  
    productList = []   
    for product in productFeatureList:
        if (product["name"] not in productList):
            productList.append(product["name"])
    return len(productList)

def getProductNumber(productName, productFeatureList):
    '''return number of product(which named as productName) in input List'''
    count = 0
    for product in productFeatureList:
        if product["name"] == productName:
            count = count + 1
    return count

def getProductTotal(productName, productFeatureList):
    '''return total price of product(which named as productName) in input List'''
    total = 0
    for product in productFeatureList:
        if product["name"] == productName:
            try:
                total = total + int(product["price"][4::])
            except:
                continue
    return total