//
//  RestRequest.swift
//  OneBank
//
//  Created by Gayuru Gunawardana on 1/12/19.
//  Copyright © 2019 iSwift. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON

protocol Refresh {
    func updateUI()
}

class RestRequest{
    
    private var _users:[User] = []
    private let mainEndPoint:String = "https://ff2fa6a4.ngrok.io/"
    private let userEndPoint:String = "https://6233b3bc.ngrok.io/users"
    private let accountEndPoint:String = "https://6233b3bc.ngrok.io/accounts"
    
    var delegate:Refresh?
    var users:[User]{
        return _users
    }
    
    private init(){
        requestPassing()
    }
    
    func requestPassing(){
        getUsers(userEndPoint)
        getUserAccounts(accountEndPoint)
    }
    
    func getUsers(_ endpoint:String){
        AF.request(endpoint,method: .get).responseJSON { (response) in
           switch response.result {
           case .success:
            let json = JSON(response.value ?? "No value")
            self.parseData(json: json)
           case let .failure(error):
               print(error)
           }
        }
    }
    
    func parseData(json:JSON){
        if json.count > 0 {
            let result = json
            for (_,v) in result{
                let firstName = v["firstName"].string
                let lastName = v["lastName"].string
                let password = v["password"].string
                let userId = v["id"].int
                let bankAccounts = v["bankAccounts"]
                var accounts:[Int] = []
                
                for(_,b) in bankAccounts{
                    accounts.append(b.int!)
                }
                
                let user = User(firstName: firstName, lastName: lastName, password: password, userID: userId,bankAccounts:accounts)
               // print(user)
            }
        }
        
    }
    
    func getUserAccounts(_ endpoint:String){
        AF.request(endpoint,method: .get).responseJSON { (response) in
           switch response.result {
           case .success:
            let json = JSON(response.value ?? "No value")
            self.parseAccountData(json: json)
           case let .failure(error):
               print(error)
           }
        }
    }
    
    func parseAccountData(json:JSON){
        if json.count > 0 {
            let result = json
            for (_,v) in result{
                let accountName = v["accountName"].string
                let accountType = v["accountType"].string
                let bankName = v["bankName"].string
                let cards = v["cards"]
                let transactions = v["transactions"]
                let verificationID = v["verificationId"].string
                let userID = v["users"].string
                
                var transactionHistory:[Int] = []
                var cardHistory:[Int] = []
                
                for(_,c) in cards{
                    cardHistory.append(c.int!)
                }
                
                for (_,t) in transactions{
                    transactionHistory.append(t.int!)
                }
//                let firstName = v["firstName"]
//               print(firstName)
            }
        }
        
    }
    
//    func getCards(dequeID:String){
//        let url = cardEndpoint + dequeID + next
//        guard let escapedAddress = url.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed)else{
//            return
//        }
//
//       getCardData(escapedAddress)
//    }
//
//    func getCardData(_ endpoint:String){
//        Alamofire.request(endpoint,method: .get).responseJSON { (response) in
//            if(response.result.isSuccess){
//                switch response.result {
//                case .success(let value):
//                    let json = JSON(value)
//                    self.parseData(json:json)
//                case .failure(let error):
//                    print(error)
//                }
//            }else{
//                print("Error: \(String(describing: response.result.error))")
//            }
//        }
//    }
//
//    func parseData(json:JSON){
//        if json.count > 0 {
//            let result = json["cards"]
//            for (_,v) in result{
//                let suit = v["suit"].string!
//                let value = v["value"].string!
//                let code = v["code"].string!
//                let imageURL = v["images"]["png"].string!
//
//                let card = Card(code: code, rank: value, suit: suit, imageURL: imageURL)
//                self._cards.append(card)
//            }
//        }
//
//        //checks if all the places are added so the arraay to notify the view
//            if self.delegate != nil{
//                DispatchQueue.main.async {
//                    self.delegate?.updateUI()
//                }
//            }
//
//    }
    static let shared = RestRequest()
    
}


