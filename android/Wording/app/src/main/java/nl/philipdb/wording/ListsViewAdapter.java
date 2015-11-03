package nl.philipdb.wording;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;

public class ListsViewAdapter extends RecyclerView.Adapter<ListsViewAdapter.ViewHolder> {
    private ArrayList<String> mListNames;

    public ListsViewAdapter(ArrayList<String> listNames) {
        mListNames = listNames;
    }

    // Create new views (invoked by the layout manager)
    @Override
    public ListsViewAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.lists_list_item_layout, parent, false);

        return new ViewHolder(v);
    }

    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        holder.mTextView.setText(mListNames.get(position));
    }

    public void addItemsToList(String[] array) {
        mListNames.addAll(Arrays.asList(array));

        // Report that the data changed
        notifyDataSetChanged();
    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mListNames.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        public TextView mTextView;

        public ViewHolder(View view) {
            super(view);
            mTextView = (TextView) view.findViewById(R.id.list_item_textview);
        }
    }
}
