package com.example.bookbook;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.NavController;
import androidx.navigation.fragment.NavHostFragment;
import androidx.navigation.ui.NavigationUI;

import com.example.bookbook.db.ResponseToken;
import com.example.bookbook.db.main.MainViewModel;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    public static final int REQUEST_IMAGE_CAPTURE = 1;
    Bitmap addOfferImage;
    private NavController navController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        BottomNavigationView bottomNav = findViewById(R.id.bottom_navigation_view);
        NavHostFragment navHostFragment =
                (NavHostFragment) getSupportFragmentManager().findFragmentById(R.id.fragment_container_view);
        navController = navHostFragment.getNavController();
        NavigationUI.setupWithNavController(bottomNav, navController);

        MainViewModel model = new ViewModelProvider(this).get(MainViewModel.class);
        model.init((ResponseToken) getIntent().getSerializableExtra(WelcomeActivity.TOKEN_MESSAGE));

        model.getAddOfferResp().observe(this,
                new toastObserver("Offer added!", R.id.add_successful));
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            Bundle extras = data.getExtras();
            addOfferImage = (Bitmap) extras.get("data");
        }
    }

    public void takePhoto() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }

//    Navigate to any fragment through action id
    public void navigateTo(int action) {
        navController.navigate(action);
    }

//    Simple observer for toasting if successful and switching fragments
    class toastObserver implements Observer<JSONObject> {
        private final String onSuccessMsg;
        private final int actionOnSuccess;

        public toastObserver(String onSuccessMsg, int actionOnSuccess) {
            this.onSuccessMsg = onSuccessMsg;
            this.actionOnSuccess = actionOnSuccess;
        }

        @Override
        public void onChanged(JSONObject response) {
            if (response == null) {
                Toast.makeText(getApplicationContext(), "server error", Toast.LENGTH_SHORT).show();
            } else if (response.has("success")) {
                navigateTo(actionOnSuccess);
                Toast.makeText(getApplicationContext(), onSuccessMsg, Toast.LENGTH_LONG).show();
            }
        }
    }

}