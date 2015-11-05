package nl.philipdb.wording;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;

public class ListsViewAdapter extends RecyclerView.Adapter<ListsViewAdapter.ViewHolder> {
    private ArrayList<List> mLists;

    public ListsViewAdapter(ArrayList<List> listNames) {
        mLists = listNames;
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
        holder.mTitle.setText(mLists.get(position).name);
        holder.mSubTitle.setText(App.getAppContext().getString(R.string.list_item_subtitle,
                mLists.get(position).language1, mLists.get(position).language2));
    }

    public void updateList(List[] lists) {
        mLists.clear();
        mLists.addAll(Arrays.asList(lists));

        // Report that the data changed
        notifyDataSetChanged();
    }

    public void addItemsToList(List[] lists) {
        mLists.addAll(Arrays.asList(lists));

        // Report that the data changed
        notifyDataSetChanged();
    }

    public void removeItem(List list) {
        mLists.remove(list);
    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mLists.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        public TextView mTitle;
        public TextView mSubTitle;

        public ViewHolder(View view) {
            super(view);
            mTitle = (TextView) view.findViewById(R.id.list_item_title);
            mSubTitle = (TextView) view.findViewById(R.id.list_item_subtitle);
        }
    }
}
