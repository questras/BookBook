package com.example.bookbook.db;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitGson {
    private static Retrofit retrofit = new Retrofit.Builder()
            .baseUrl("https://127.0.0.1:8000/api/auth/")
            .addConverterFactory(GsonConverterFactory.create())
            .build();


    public static <T> T createService(Class<T> serviceClass) {
        return retrofit.create(serviceClass);
    }
}
