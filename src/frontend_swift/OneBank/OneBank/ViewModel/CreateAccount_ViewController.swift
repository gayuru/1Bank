//
//  CreateAccount.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//


import UIKit
import MobileCoreServices
import FileBrowser

class CreateAccount_ViewController: UIViewController,UIPickerViewDataSource,UIPickerViewDelegate{

    @IBOutlet weak var pickerTextField: UITextField!
    
    let accountTypes = ["Savings","Cheque","Credit"]
    
    var bankName:String!
    
    @IBOutlet weak var accountName: UITextField!
    
    @IBAction func createAccount(_ sender: Any) {
        print("Create account details")
        print(bankName!)
        print(accountName.text!)
        print(pickerTextField.text!)
    }
    

    func numberOfComponents(in pickerView:UIPickerView)-> Int{
        return 1
    }
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return accountTypes[row]
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return accountTypes.count
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        //shows the picked element
        pickerTextField.text = accountTypes[row]
    }
    
    func createPickerView(){
        let pickerView = UIPickerView()
        pickerView.delegate = self
        pickerTextField.inputView = pickerView
        
    }
    
    func dismissPicker(){
        let toolbar = UIToolbar()
        toolbar.sizeToFit()
        
        let doneButton = UIBarButtonItem(title: "Done", style: .plain, target: self, action: #selector(self.dismissKeyboard))
        
        toolbar.setItems([doneButton], animated: false)
        toolbar.isUserInteractionEnabled = true
        pickerTextField.inputAccessoryView = toolbar
    }
   
    @objc func dismissKeyboard(){
        view.endEditing(true)
    }
    
    @IBAction func uploadDocumentBtn(_ sender: Any) {
       let fileBrowser = FileBrowser()
       present(fileBrowser, animated: true, completion: nil)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        createPickerView()
        dismissPicker()
        // Do any additional setup after loading the view.
    }


}




