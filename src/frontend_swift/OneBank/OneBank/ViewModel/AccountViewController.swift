//
//  AccountViewController.swift
//  OneBank
//
//  Created by Sogyal Thundup Sherpa on 1/12/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class AccountViewController: UIViewController {

    @IBOutlet weak var bankView: UIView!
    var currentAccount:String!
    override func viewDidLoad() {
        super.viewDidLoad()
        overrideUserInterfaceStyle = .light
        bankView.layer.cornerRadius = 50
        bankView.layer.maskedCorners = [.layerMinXMaxYCorner]
        
        switch currentAccount {
        case "CBA":
            self.bankView.backgroundColor = UIColor(red: 255, green: 204, blue: 0)
        case "NAB":
            self.bankView.backgroundColor = UIColor(red: 190, green: 13, blue: 0)
        default:
            self.bankView.backgroundColor = UIColor.white
        }
        // Do any additional setup after loading the view.
    }

}
