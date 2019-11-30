//
//  TransferViewController.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 1/12/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class TransferViewController: UIViewController {

    @IBOutlet weak var userOne: UIButton!
    @IBOutlet weak var userTwo: UIButton!
    @IBOutlet weak var userThree: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        userOne.layer.cornerRadius = userOne.frame.size.width / 2
              userOne.clipsToBounds = true
        
        userTwo.layer.cornerRadius = userTwo.frame.size.width / 2
              userTwo.clipsToBounds = true
        
        
        userThree.layer.cornerRadius = userThree.frame.size.width / 2
              userThree.clipsToBounds = true
        // Do any additional setup after loading the view.
    }


}
