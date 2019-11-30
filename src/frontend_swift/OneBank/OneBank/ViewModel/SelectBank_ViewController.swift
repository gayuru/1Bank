//
//  SelectBank_ViewController.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 30/11/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class SelectBank_ViewController: UIViewController {

    var isOptionNew:Bool!
    private var bankSelected:String = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

}

extension SelectBank_ViewController{

     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
               
    if(segue.identifier == "createAccount"){
        let createAccountController = segue.destination as! CreateAccount_ViewController
        if(!bankSelected.isEmpty){
            createAccountController.bankName = bankSelected
        }
    }else if(segue.identifier == "existingAccount"){
        let existingAccountController = segue.destination as! ExistingAccount_ViewController
        if(!bankSelected.isEmpty){
           existingAccountController.bankName = bankSelected
        }
    }
}
    
    @IBAction func createAccount(_ sender: Any)
    {
        var designatedView:String = "existingAccount"
        
        if(isOptionNew){
            designatedView = "createAccount"
        }
        
        let btn = sender as! UIButton
        switch btn.tag{
        case 1:
            self.bankSelected = "combank"
            performSegue(withIdentifier: designatedView, sender: self)
            break;
        case 2:
            self.bankSelected = "nab"
            performSegue(withIdentifier: designatedView, sender: self)
            break;
        case 3:
            self.bankSelected = "anz"
            performSegue(withIdentifier: designatedView, sender: self)
            break;
        case 4:
            self.bankSelected = "westpac"
            performSegue(withIdentifier: designatedView, sender: self)
            break;
        default:
            break;
            
        }
    }
    

    
}
