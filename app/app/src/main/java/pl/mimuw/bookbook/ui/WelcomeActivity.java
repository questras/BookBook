package pl.mimuw.bookbook.ui;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;
import androidx.lifecycle.ViewModelProvider;

import pl.mimuw.bookbook.R;

import pl.mimuw.bookbook.db.sign.SignViewModel;

public class WelcomeActivity extends AppCompatActivity implements NavigationHost {

    private SignViewModel model;
    public static final String TOKEN_MESSAGE = "pl.mimuw.android.twoactivities.extra.token";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        model = new ViewModelProvider(this).get(SignViewModel.class);
        model.init();
        model.getToken().observe(this, response -> {
            if (response == null) {
                Toast.makeText(getApplicationContext(), "server error", Toast.LENGTH_SHORT).show();
            } else if (response.first != null) { // deserialization success, token available
                switchToMain();
            }
        });

        model.getRegisterResp().observe(this, response -> {
            if (response == null) {
                Toast.makeText(getApplicationContext(), "server error", Toast.LENGTH_SHORT).show();
            } else if (response.has("success")) {
                navigateTo(new SignIn(), true);
                Toast.makeText(getApplicationContext(), "user created", Toast.LENGTH_LONG).show();
            }
        });

        if (savedInstanceState == null) {
            getSupportFragmentManager()
                    .beginTransaction()
                    .add(R.id.fragment_container_view, new SignIn())
                    .setReorderingAllowed(true)
                    .commit();
        }
    }

    @Override
    public void navigateTo(Fragment fragment, boolean addToBackStack) {
        FragmentTransaction transaction = getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.fragment_container_view, fragment)
                .setReorderingAllowed(true);
        if (addToBackStack)
            transaction.addToBackStack(null);
        transaction.commit();
    }

    public void switchToMain() {
        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        intent.putExtra(TOKEN_MESSAGE, model.getToken().getValue().first);
        startActivity(intent);
        finish();
    }
}