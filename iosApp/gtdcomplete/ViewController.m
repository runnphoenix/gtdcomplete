//
//  ViewController.m
//  gtdcomplete
//
//  Created by temp on 2018/2/25.
//  Copyright © 2018年 self. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    //login first
    //    NSDictionary *dic = [NSDictionary dictionaryWithObjects:@[@"runnphoenix",@"runn2reborngc"] forKeys:@[@"username",@"password"]];
    //    //NSDictionary *dic = [NSDictionary dictionaryWithObjects:@[@"oldman",@"123"] forKeys:@[@"username",@"password"]];
    //    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:dic options:NSJSONWritingPrettyPrinted error:nil];
    //    NSURL *url = [NSURL URLWithString:@"https://gtdcomplete-171902.appspot.com/login.json"];
    //    //NSURL *url = [NSURL URLWithString:@"http://localhost:8080/login.json"];
    //    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    //    [request setHTTPMethod:@"POST"];
    //    [request setHTTPBody:jsonData];
    //    NSURLSession *session = [NSURLSession sharedSession];
    //    NSURLSessionDataTask *task = [session dataTaskWithRequest:request completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
    //        NSString *str = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
    //        NSLog(@"%@",str);
    //        // save user_id
    //        NSDictionary *jsonDic = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:nil];
    //        NSString *user_id = [jsonDic objectForKey:@"uid"];
    //        NSLog(@"%@",user_id);
    //        [[NSUserDefaults standardUserDefaults] setObject:user_id forKey:@"uid"];
    //    }];
    //    [task resume];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
