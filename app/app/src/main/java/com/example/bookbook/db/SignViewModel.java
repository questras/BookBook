package com.example.bookbook.db;

import android.util.Pair;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import org.json.JSONObject;

public class SignViewModel extends ViewModel {

    private MutableLiveData<Pair<ResponseToken, JSONObject>> data;
    private SignRepository signRepository;

    public void init() {
        if (signRepository != null) {
            return;
        }
        signRepository = SignRepository.getInstance();
        data = new MutableLiveData<>();
    }

    public LiveData<Pair<ResponseToken, JSONObject>> getResponse() {
        return data;
    }

    public void authenticate(String email, String pass) {
        signRepository.authenticate(email, pass, data);
    }

}
