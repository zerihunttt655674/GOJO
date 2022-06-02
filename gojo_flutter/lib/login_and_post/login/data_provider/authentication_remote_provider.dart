import 'package:gojo_flutter/login_and_post/login/data_provider/Authentication_provider.dart';
import 'package:http/http.dart' as http;


class AuthenticationRemote implements AuthenticationProvider {
  final _uri = Uri.parse("http://local_host/uer/login");
  @override
  Future<http.Response> authenticateUser(
      String username, String password) async {
    

    try {
      final response = await http.post(_uri, body: {
        'username': username,
        'password': password,
      });
      return response;
    } catch (err) {
      throw Exception("failed to connect");
    }
  }

  // @override
  // Future<void> registerUser(User user) {
  //   return ;
  // }
}
