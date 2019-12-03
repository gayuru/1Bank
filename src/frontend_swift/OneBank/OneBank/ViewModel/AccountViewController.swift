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
    @IBOutlet weak var accountName: UILabel!
    @IBOutlet weak var transactionTableView: UITableView!
    private var placeNames : [String] = []
    private var placeImages : [String] = []
    private var placeExpenses : [String] = []
    override func viewDidLoad() {
        super.viewDidLoad()
        overrideUserInterfaceStyle = .light
        accountsCardCollection.delegate = self
        accountsCardCollection.dataSource = self
        transactionTableView.delegate = self
        transactionTableView.dataSource = self
        transactionTableView.allowsSelection = false
        bankView.layer.cornerRadius = 50
        bankView.layer.maskedCorners = [.layerMinXMaxYCorner]
        accountsCardCollection.layer.maskedCorners = [.layerMinXMaxYCorner]
        accountsCardCollection.backgroundColor = UIColor.clear
        setup()
        switch currentAccount {
        case "CBA":
            self.accountName.text = "Commonwealth Bank Of Australia"
            self.bankView.backgroundColor = UIColor(red: 255, green: 204, blue: 0)
        case "NAB":
            self.accountName.text = "National Bank Of Austrailia"
            self.bankView.backgroundColor = UIColor(red: 190, green: 13, blue: 0)
        case "WSP":
            self.accountName.text = "WestPac"
            self.bankView.backgroundColor = UIColor(red: 10, green: 20, blue: 20)
        case "ANZ":
            self.accountName.text = "Austrlia New Zealand Bank"
            self.bankView.backgroundColor = UIColor(red:0.58, green:0.80, blue:1.00, alpha:1.0)
        default:
            self.bankView.backgroundColor = UIColor.white
        }
        // Do any additional setup after loading the view.
    }

    private func setup(){
        placeNames.append("Uber Eats")
        placeNames.append("Mc Donalds")
        placeNames.append("Spotify")
        placeNames.append("Telstra")
        placeNames.append("KFC")
        placeImages.append("ubereats")
        placeImages.append("maccas")
        placeImages.append("spotify")
        placeImages.append("telstra")
        placeImages.append("kfc")
        placeExpenses.append("$14.00")
        placeExpenses.append("$20.00")
        placeExpenses.append("$10.00")
        placeExpenses.append("$40.00")
        placeExpenses.append("$20.00")
        
    }

}

extension AccountViewController:UICollectionViewDelegate,UICollectionViewDataSource{
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 6
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cardCell", for: indexPath) as! AccountsCardCollectionViewCell
        
        if indexPath.row/2 == 0{
            cell.balanceLabel.text = "14.00"
            cell.cardNumber.text! = "**** **** **** 1422)"
            cell.cardType.image = UIImage(named: "visa")
        }else{
            cell.balanceLabel.text = "4.00"
            cell.cardNumber.text! = "**** **** **** 1451)"
            cell.cardType.image = UIImage(named: "mastercard")
        }
        return cell
    }
}


extension AccountViewController:UITableViewDelegate,UITableViewDataSource{
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return placeNames.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "transactionCell", for: indexPath) as! TransactionsTableViewCell
        cell.companyLogo.image = UIImage(named:placeImages[indexPath.row])
        cell.companyNameLabel.text = placeNames[indexPath.row]
        cell.amountSpendLabel.text = placeExpenses[indexPath.row]
        if indexPath.row/2 == 0{
            cell.timeAgoLabel.text = "20 hours ago"
        }else{
            cell.timeAgoLabel.text = "2 days ago"
        }
        return cell
    }
}
