package pl.mimuw.bookbook.db.main;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

public class Offer {
    public static final String activeStatus = "AC";
    private int id;
    private URL imageUrl;
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
        try {
            this.imageUrl = new URL(image);
        } catch (MalformedURLException e) {
            this.imageUrl = null;
        }
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

    public URL getImageUrl() {
        return imageUrl;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getDescription() {
        return description;
    }

    public String getState() {
        return state;
    }

    public String getCity() {
        return city;
    }

    public String getLenderEmail() {
        return lenderEmail;
    }

    public String getLenderPhone() {
        return lenderPhone;
    }
}
