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
    @IBOutlet weak var accountsCardCollection: UICollectionView!
    override func viewDidLoad() {
        super.viewDidLoad()
        overrideUserInterfaceStyle = .light
        bankView.layer.cornerRadius = 50
        bankView.layer.maskedCorners = [.layerMinXMaxYCorner]
        
        accountsCardCollection.delegate = self
        accountsCardCollection.dataSource = self
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

extension AccountViewController:UICollectionViewDelegate,UICollectionViewDataSource{
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 3
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cardCell", for: indexPath) as! AccountsCardCollectionViewCell
        cell.balanceLabel.text = "14.000"
        cell.cardNumber.text! + "**** **** **** 1422)"
        cell.cardTypeLabel.text = "VISA"
        
        return cell
    }
    
    
}
