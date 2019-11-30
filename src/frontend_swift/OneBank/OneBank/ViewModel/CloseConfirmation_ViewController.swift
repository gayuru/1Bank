//
//  CloseBankAccountConfirmation_ViewController.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 1/12/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class CloseConfirmation_ViewController: UIViewController {

    var bankAccount:String!
    
    @IBOutlet weak var closeAccount: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(bankAccount)
        closeAccount.layer.borderWidth = 1.0
        closeAccount.layer.borderColor = UIColor(red:0.24, green:0.19, blue:0.75, alpha:1.0).cgColor
        // Do any additional setup after loading the view.
    }
    
    


}
