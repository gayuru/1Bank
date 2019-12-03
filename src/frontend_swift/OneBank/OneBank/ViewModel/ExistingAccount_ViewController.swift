//
//  ExistingAccount_ViewController.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class ExistingAccount_ViewController: UIViewController {
 
    var bankName:String!
    
    @IBOutlet weak var accountName: UITextField!
    @IBOutlet weak var accountNumber: UITextField!
    @IBOutlet weak var verificationToken: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let userTappedOtherThanKeyboard: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: Selector(("closeKeyboard")))
        view.addGestureRecognizer(userTappedOtherThanKeyboard)
        // Do any additional setup after loading the view.
    }


    @IBAction func addAccount(_ sender: Any) {
        print(accountName.text!)
        print(accountNumber.text!)
        print(verificationToken.text!)
        print(bankName!)
    }
    
    @objc func closeKeyboard() {
      view.endEditing(true)
   }
}

