package pl.mimuw.bookbook.ui;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModelProvider;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import pl.mimuw.bookbook.R;

import pl.mimuw.bookbook.db.main.MainViewModel;
import com.google.android.material.button.MaterialButton;

import org.json.JSONObject;

public class UserProfile extends Fragment {
    private TextView email;
    private TextView username;

    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_user_profile, container, false);
        ImageButton likeButton = view.findViewById(R.id.like_button);
        ImageButton dislikeButton = view.findViewById(R.id.dislike_button);
        MaterialButton historyButton = view.findViewById(R.id.user_history_button);
        MaterialButton signOutButton = view.findViewById(R.id.sign_out_button);
        MainViewModel model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
        username = view.findViewById(R.id.username);
        email = view.findViewById(R.id.mail_text);
        MutableLiveData<JSONObject> userInfo = new MutableLiveData<>();
        userInfo.observe(requireActivity(), this::setUserData);
        model.getUserInfo(userInfo);

        likeButton.setOnClickListener(new View.OnClickListener() {
            private boolean liked = false;
            @Override
            public void onClick(View v) {
                if (liked)
                    likeButton.setImageResource(R.drawable.ic_like);
                else
                    likeButton.setImageResource(R.drawable.ic_liked);
                liked = !liked;
            }
        });

        dislikeButton.setOnClickListener(new View.OnClickListener() {
            private boolean disliked = false;
            @Override
            public void onClick(View v) {
                if (disliked)
                    dislikeButton.setImageResource(R.drawable.ic_dislike);
                else
                    dislikeButton.setImageResource(R.drawable.ic_disliked);
                disliked = !disliked;
            }
        });

        historyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                TODO
            }
        });

        signOutButton.setOnClickListener(v -> model.signOut());

        return view;
    }

    private void setUserData(JSONObject data) {
        if (data.has("id")) {
            email.setText(data.optString("email"));
            username.setText(String.format("%s %s", data.optString("first_name"), data.optString("last_name")));
        } else {
            Toast.makeText(requireActivity(), "Cannot fetch user data", Toast.LENGTH_SHORT).show();
        }
    }

}