package com.example.bookbook;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

import com.example.bookbook.db.main.MainViewModel;
import com.google.android.material.button.MaterialButton;

public class UserProfile extends Fragment {
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_user_profile, container, false);
        ImageButton likeButton = view.findViewById(R.id.like_button);
        ImageButton dislikeButton = view.findViewById(R.id.dislike_button);
        MaterialButton historyButton = view.findViewById(R.id.user_history_button);
        MaterialButton signOutButton = view.findViewById(R.id.sign_out_button);
        MainViewModel model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);

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

}