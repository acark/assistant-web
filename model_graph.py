from django.apps import apps
import pygraphviz as pgv

def generate_restaurant_model_graph(output_file='restaurant_models.png'):
    # Create a new directed graph
    graph = pgv.AGraph(directed=True, rankdir="LR")

    # Get the restaurants app
    restaurants_app = apps.get_app_config('restaurants')

    # Get all models from the restaurants app
    for model in restaurants_app.get_models():
        # Add a node for each model
        graph.add_node(model.__name__, shape="box")

        # Add model fields as a label
        field_labels = [f"{field.name}: {field.get_internal_type()}" for field in model._meta.fields]
        graph.get_node(model.__name__).attr['label'] = f"{model.__name__}\n" + "\n".join(field_labels)

        # Add edges for foreign key relationships
        for field in model._meta.fields:
            if field.is_relation:
                related_model = field.related_model
                if related_model._meta.app_label == 'restaurants':
                    if field.many_to_one:
                        graph.add_edge(model.__name__, related_model.__name__, label=field.name)
                    elif field.one_to_one:
                        graph.add_edge(model.__name__, related_model.__name__, dir="both", label=field.name)

        # Add edges for many-to-many relationships
        for field in model._meta.many_to_many:
            related_model = field.related_model
            if related_model._meta.app_label == 'restaurants':
                graph.add_edge(model.__name__, related_model.__name__, dir="both", style="dashed", label=field.name)
                
                
    

    # Layout the graph
    graph.layout(prog='dot')
    print("Ses")
    # Save the graph
    graph.draw(output_file)

    print(f"Graph saved to {output_file}")

# Usage
if __name__ == "__main__":
    generate_restaurant_model_graph()