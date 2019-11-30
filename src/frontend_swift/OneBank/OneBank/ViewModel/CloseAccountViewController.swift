//
//  CloseAccountViewController.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 1/12/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import Foundation
import UIKit

class CloseAccountViewController:UIViewController,UIPickerViewDataSource,UIPickerViewDelegate{
    
    @IBOutlet weak var bankAccountList: UITextField!
    
    let accountTypes = ["NAB: 123 456 789","Combank: 123 456 789","ANZ: 123 456 789"]
    
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
         bankAccountList.text = accountTypes[row]
     }
     
     func createPickerView(){
         let pickerView = UIPickerView()
         pickerView.delegate = self
         bankAccountList.inputView = pickerView
         
     }
     
     func dismissPicker(){
         let toolbar = UIToolbar()
         toolbar.sizeToFit()
         
         let doneButton = UIBarButtonItem(title: "Done", style: .plain, target: self, action: #selector(self.dismissKeyboard))
         
         toolbar.setItems([doneButton], animated: false)
         toolbar.isUserInteractionEnabled = true
         bankAccountList.inputAccessoryView = toolbar
     }
    
     @objc func dismissKeyboard(){
         view.endEditing(true)
     }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        bankAccountList.backgroundColor = UIColor.clear
        bankAccountList.layer.borderWidth = 1.0
        bankAccountList.layer.borderColor = UIColor(red:0.24, green:0.19, blue:0.75, alpha:1.0).cgColor
        createPickerView()
        dismissPicker()

    }
}

extension CloseAccountViewController{
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if(segue.identifier == "confirmation"){
            let confirmationController = segue.destination as! CloseConfirmation_ViewController
            confirmationController.bankAccount = bankAccountList.text
        }
    }
}
