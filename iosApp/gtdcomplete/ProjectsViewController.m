//
//  ProjectsViewController.m
//  gtdcomplete
//
//  Created by temp on 2018/2/25.
//  Copyright © 2018年 self. All rights reserved.
//

#import "ProjectsViewController.h"

@interface ProjectsViewController ()

@end

@implementation ProjectsViewController{
    NSArray *_projects;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.tableView.dataSource = self;
    
    // Look up projects data
    NSString *uud = [[NSUserDefaults standardUserDefaults] objectForKey:@"uid"];
    NSLog(@"%@", uud);
    if (uud != nil){
        NSDictionary *dic2 = [NSDictionary dictionaryWithObjects:@[uud] forKeys:@[@"uid"]];
        NSData *jsonData2 = [NSJSONSerialization dataWithJSONObject:dic2 options:NSJSONWritingPrettyPrinted error:nil];
        NSURL *url2 = [NSURL URLWithString:@"https://gtdcomplete-171902.appspot.com/projects.json"];
        //NSURL *url2 = [NSURL URLWithString:@"http://localhost:8080/projects.json"];
        NSMutableURLRequest *request2 = [NSMutableURLRequest requestWithURL:url2];
        [request2 setHTTPMethod:@"POST"];
        [request2 setHTTPBody:jsonData2];
        NSURLSession *session2 = [NSURLSession sharedSession];
        NSURLSessionDataTask *task2 = [session2 dataTaskWithRequest:request2 completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
            NSString *str = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
            NSLog(@"%@", str);
            NSDictionary *projects_dic = [NSJSONSerialization JSONObjectWithData:data
                                                                         options:NSJSONReadingAllowFragments
                                                                           error:nil];
            _projects = [projects_dic allValues];
            _projects = _projects[0];
            NSLog(@"%@", _projects);
            dispatch_async(dispatch_get_main_queue(), ^{
                [self.tableView reloadData];
            });
        }];
        [task2 resume];
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return _projects.count;
}


- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"reuseIdentifier"];
    
    if (cell == nil) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:@"reuseIdentifier"];
    }
    
    cell.textLabel.text = [_projects[indexPath.row] description];
    
    return cell;
}


/*
// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath {
    // Return NO if you do not want the specified item to be editable.
    return YES;
}
*/

/*
// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath {
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        // Delete the row from the data source
        [tableView deleteRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationFade];
    } else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }   
}
*/

/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath {
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath {
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
