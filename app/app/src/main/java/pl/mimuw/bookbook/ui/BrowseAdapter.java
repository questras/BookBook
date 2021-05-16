package pl.mimuw.bookbook.ui;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.RecyclerView;

import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;

import pl.mimuw.bookbook.R;
import pl.mimuw.bookbook.db.main.MainViewModel;
import pl.mimuw.bookbook.db.main.Offer;

import static java.util.concurrent.Executors.newCachedThreadPool;

public class BrowseAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {

    private final int VIEW_TYPE_ITEM = 0;
    private final int VIEW_TYPE_LOADING = 1;
    private final Context context;
    private final ExecutorService threadPool;
    public ArrayList<Offer> offers;

    public BrowseAdapter(Context context) {
        this.context = context;
        offers = new ArrayList<>();
        threadPool = newCachedThreadPool();
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        if (viewType == VIEW_TYPE_ITEM) {
            View view = LayoutInflater.from(parent.getContext()).
                    inflate(R.layout.offer_view, parent, false);
            return new ItemViewHolder(view);
        } else {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_loading,
                    parent, false);
            return new LoadingViewHolder(view);
        }
    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder holder, int position) {
        if (holder instanceof ItemViewHolder) {
            populateItems((ItemViewHolder) holder, position);
        }
    }

    @Override
    public int getItemCount() {
        return offers.size() + 1;
    }

    @Override
    public int getItemViewType(int position) {
        return position == offers.size() ? VIEW_TYPE_LOADING : VIEW_TYPE_ITEM;
    }

    private void populateItems(@NonNull ItemViewHolder holder, int position) {
        holder.position = position;
        holder.title.setText(offers.get(position).getTitle());
        holder.author.setText(offers.get(position).getAuthor());
        URL imageUrl = offers.get(position).getImageUrl();
        if (imageUrl != null) {
            threadPool.execute(new SetImage(holder.book, imageUrl, position));
        }
    }

    private static class LoadingViewHolder extends RecyclerView.ViewHolder {
        ProgressBar progressBar;

        public LoadingViewHolder(@NonNull View itemView) {
            super(itemView);
            progressBar = itemView.findViewById(R.id.progressBar);
        }
    }

    private class ItemViewHolder extends RecyclerView.ViewHolder {
        private final TextView title;
        private final TextView author;
        private final ImageView book;
        private int position = -1; // indicates no position assigned yet

        public ItemViewHolder(@NonNull View view) {
            super(view);
            book = view.findViewById(R.id.book_image);
            author = view.findViewById(R.id.author);
            title = view.findViewById(R.id.title);

            view.setOnClickListener(v -> {
                if (position >= 0) {
                    Bundle toSend = new Bundle();
                    toSend.putInt("position", position);
                    ((MainActivity) context).navigateWithData(R.id.view_offer, toSend);
                }
            });
        }
    }

    private class SetImage implements Runnable {
        private final ImageView toSet;
        private final URL imageUrl;
        private final int position;

        public SetImage(ImageView toSet, URL imageUrl, int position) {
            this.toSet = toSet;
            this.imageUrl = imageUrl;
            this.position = position;
        }

        @Override
        public void run() {
            try {
                Bitmap image = BitmapFactory.decodeStream(imageUrl.openConnection().getInputStream());
                new ViewModelProvider((MainActivity) context).get(MainViewModel.class).addOfferImage(image, position);
                ((Activity) context).runOnUiThread(() -> {
                    toSet.setImageBitmap(Bitmap.createScaledBitmap(image, 500, 500, true));
                });
            } catch (IOException e) {
                Log.d("Internet", "Cannot download image");
            }
        }
    }
}
