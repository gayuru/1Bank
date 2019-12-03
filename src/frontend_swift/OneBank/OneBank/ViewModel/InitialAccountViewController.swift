//
//  InitialViewController.swift
//  
//
//  Created by Gayuru Gunawardana on 1/12/19.
//

import UIKit

class InitialAccountViewController: UIViewController {
    
    @IBOutlet weak var existingBankBtn: UIButton!
    @IBOutlet weak var usernameLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        usernameLabel.text = Globals.username
        overrideUserInterfaceStyle = .light
        existingBankBtn.layer.borderWidth = 1.0
        existingBankBtn.layer.borderColor = UIColor(red:0.24, green:0.19, blue:0.75, alpha:1.0).cgColor
        // Do any additional setup after loading the view.
    }
    
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
