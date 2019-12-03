//
//  AccountsViewController.swift
//  OneBank
//
//  Created by Sogyal Thundup Sherpa on 1/12/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import UIKit

class AccountsViewController: UIViewController
{

    @IBOutlet weak var accountsView: UIView!
    @IBOutlet weak var accountsCollectionView: UICollectionView!
    private var accountSelected:String!
    override func viewDidLoad() {
        super.viewDidLoad()
        overrideUserInterfaceStyle = .light
        accountsCollectionView.delegate = self
        accountsCollectionView.dataSource = self
        accountsView.layer.cornerRadius = 50
        accountsView.layer.maskedCorners = [.layerMinXMinYCorner,.layerMaxXMinYCorner]
        accountsView.clipsToBounds = true
    }
    
    
    //TODO:Before the next screen is shown
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "goToAccount" {
            let accountVC = segue.destination as! AccountViewController
            accountVC.currentAccount = self.accountSelected
        }
    }

}

extension AccountsViewController:UICollectionViewDelegate,UICollectionViewDataSource{
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 6
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "accountCell", for: indexPath) as! AccountsCollectionViewCell
        if indexPath.row / 2 == 0 {
            cell.bankNameLabel.text = "Commonwealth Bank"
            cell.accountImage.image = UIImage(named: "combank_logo")
        }else{
            cell.bankNameLabel.text = "NAB"
            cell.accountImage.image = UIImage(named: "nab_logo")
        }

        cell.bankBalance.text = "$300.00"
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        if indexPath.row / 2 == 0{
            accountSelected = "CBA"
        }else{
            accountSelected = "NAB"
        }
        self.performSegue(withIdentifier: "goToAccount", sender: self)
    }
    
    
}
