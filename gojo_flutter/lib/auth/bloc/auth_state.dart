import 'package:equatable/equatable.dart';

import '../model/model.dart';

abstract class AuthState extends Equatable {
  @override
  // TODO: implement props
  List<Object?> get props => [];
}

class Idle extends AuthState {}

class LoginIn extends AuthState {}

class LoginSuccessful extends AuthState {
  User userId;
  LoginSuccessful(this.userId);
}

class LoginFailed extends AuthState {
  String? error;
  LoginFailed(this.error);
}

class SigningIn extends AuthState {}

class SigninSuccessful extends AuthState {}

class SigninFailed extends AuthState {}

class UserUpdating extends AuthState {}

class UserUpdateSuccess extends AuthState {}

class UserUpdateFailuer extends AuthState {}