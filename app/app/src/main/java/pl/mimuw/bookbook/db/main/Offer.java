package pl.mimuw.bookbook.db.main;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;

public class Offer {
    public static final String activeStatus = "AC";
    private int id;
    private String image;
    private String title;
    private String author;
    private String description;
    private String state;
    private String city;
    private String lenderEmail;
    private String lenderFirstName;
    private String lenderSecondName;
    private String lenderPhone;

    public Offer(int id, String image, String title, String author, String description,
                 String state, String city, String lenderEmail, String lenderFirstName,
                 String lenderSecondName, String lenderPhone) {
        this.id = id;
        this.image = image;
        this.title = title;
        this.author = author;
        this.description = description;
        this.state = state;
        this.city = city;
        this.lenderEmail = lenderEmail;
        this.lenderFirstName = lenderFirstName;
        this.lenderSecondName = lenderSecondName;
        this.lenderPhone = lenderPhone;
    }

    public Bitmap getImage(String src) {
        try {
            java.net.URL url = new java.net.URL(src);
            HttpURLConnection connection = (HttpURLConnection) url
                    .openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            Bitmap myBitmap = BitmapFactory.decodeStream(input);
            return myBitmap;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
