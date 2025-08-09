using Google.Cloud.Firestore;

namespace JobSite.Models
{
    public class Listener(FirestoreDb db)
    {
        public void Listen(string coll_name)
        {
            CollectionReference citiesRef = db.Collection(coll_name);

            FirestoreChangeListener listener = citiesRef.Listen(snapshot =>
            {
                foreach (DocumentSnapshot documentSnapshot in snapshot.Documents)
                {
                    Console.WriteLine(documentSnapshot.Id);
                }
            });
        }
    }
}
