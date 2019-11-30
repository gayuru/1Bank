//
//  InitialAccount_ViewController.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class InitialAccount_ViewController: UIViewController {

    @IBOutlet weak var existingBankBtn: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        existingBankBtn.layer.borderWidth = 1.0
        existingBankBtn.layer.borderColor = UIColor(red:0.24, green:0.19, blue:0.75, alpha:1.0).cgColor
        // Do any additional setup after loading the view.
    }
}

extension InitialAccount_ViewController{
       override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
           if(segue.identifier == "createAccount"){
               let bankController = segue.destination as! SelectBank_ViewController
               bankController.isOptionNew = true
           }else if(segue.identifier == "existingAccount"){
               let bankController = segue.destination as! SelectBank_ViewController
               bankController.isOptionNew = false
           }
       }
   }