package com.example.bookbook.db;

public class RequestToken {
    private final String email;
    private final String password;
    private final String device;

    public RequestToken(String email, String password, String device) {
        this.email = email;
        this.password = password;
        this.device = device;
    }
}
