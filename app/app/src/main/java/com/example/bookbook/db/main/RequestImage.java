package com.example.bookbook.db.main;

public class RequestImage {
    private int offerId;
    private byte[] image;

    public RequestImage(int offerId, byte[] image) {
        this.offerId = offerId;
        this.image = image;
    }
}
