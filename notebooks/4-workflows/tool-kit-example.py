from typing import Dict, List, Set, Any, Callable, TypedDict
import networkx as nx
from langgraph.graph import StateGraph

class GraphState(TypedDict):
    """State for the graph execution"""
    inputs: Dict[str, Any]  # Input values
    outputs: Dict[str, Any]  # Output values produced by nodes
    execution_order: List[str]  # Order of nodes executed


class GraphNode:
    def __init__(self, name: str, process_func: Callable):
        """
        Initialize a graph node representing a LangGraph processor

        Args:
            name: Unique identifier for this graph
            process_func: Function that executes this graph's logic
        """
        self.name = name
        self.process_func = process_func
        self.produces = []  # Outputs this graph produces
        self.requires = []  # Inputs this graph requires
        self.optional_inputs = []  # Inputs that are optional for this graph
        
        # Added fields for type and description information
        self.input_types = {}  # Dict mapping input name -> type
        self.output_types = {}  # Dict mapping output name -> type
        self.input_descriptions = {}  # Dict mapping input name -> description
        self.output_descriptions = {}  # Dict mapping output name -> description

    def __repr__(self):
        return f"GraphNode({self.name}, produces={self.produces}, requires={self.requires})"
        
    def add_input(self, name: str, required: bool = True, type_hint: str = "Any", description: str = ""):
        """
        Add an input field with type and description
        
        Args:
            name: Name of the input field
            required: Whether this input is required (True) or optional (False)
            type_hint: String representation of the input type
            description: Description of what this input is used for
        """
        if required and name not in self.requires:
            self.requires.append(name)
        elif not required and name not in self.optional_inputs:
            self.optional_inputs.append(name)
            
        self.input_types[name] = type_hint
        self.input_descriptions[name] = description
        
    def add_output(self, name: str, type_hint: str = "Any", description: str = ""):
        """
        Add an output field with type and description
        
        Args:
            name: Name of the output field
            type_hint: String representation of the output type
            description: Description of what this output contains
        """
        if name not in self.produces:
            self.produces.append(name)
            
        self.output_types[name] = type_hint
        self.output_descriptions[name] = description


class DependencyManager:
    def __init__(self):
        """Initialize the dependency manager that tracks graph dependencies"""
        self.graphs = {}  # name -> GraphNode
        self.output_producers = {}  # output_name -> producing_graph_name
        self.dependency_graph = nx.DiGraph()  # Graph node dependencies

    def register_graph(self, graph_node: GraphNode) -> None:
        """
        Register a graph and its outputs/requirements

        Args:
            graph_node: The graph node to register
        """
        self.graphs[graph_node.name] = graph_node

        # Add node to dependency graph
        self.dependency_graph.add_node(graph_node.name)

        # Register what outputs this graph produces
        for output in graph_node.produces:
            if output in self.output_producers:
                raise ValueError(f"Output '{output}' is already produced by graph '{self.output_producers[output]}'")
            self.output_producers[output] = graph_node.name

    def build_dependency_edges(self) -> None:
        """
        Build edges between graph nodes based on input/output dependencies
        Call this after registering all graphs
        """
        for graph_name, graph_node in self.graphs.items():
            for required_input in graph_node.requires:
                if required_input in self.output_producers:
                    producer_graph = self.output_producers[required_input]
                    # Add edge from producer to consumer
                    self.dependency_graph.add_edge(producer_graph, graph_name)

    def check_circular_dependencies(self) -> None:
        """Check for circular dependencies in the graph"""
        try:
            nx.find_cycle(self.dependency_graph)
            cycles = list(nx.simple_cycles(self.dependency_graph))
            raise ValueError(f"Circular dependencies detected: {cycles}")
        except nx.NetworkXNoCycle:
            # No cycle found, this is good
            pass

    def resolve_dependencies(self, desired_outputs: List[str]) -> List[str]:
        """
        Determine which graphs are needed and their execution order

        Args:
            desired_outputs: List of output names the user wants

        Returns:
            Ordered list of graph names to execute
        """
        # Find graphs that directly produce desired outputs
        required_graphs = set()
        output_producers = {}

        # First identify all graphs that produce the desired outputs
        for output in desired_outputs:
            if output not in self.output_producers:
                raise ValueError(f"No graph produces output '{output}'")

            producer = self.output_producers[output]
            required_graphs.add(producer)
            output_producers[output] = producer

        # Now find all dependencies of the required graphs
        all_dependencies = set()
        for graph_name in required_graphs:
            # Find all predecessors (graphs that must run before this one)
            predecessors = nx.ancestors(self.dependency_graph, graph_name)
            all_dependencies.update(predecessors)

        # Combine direct producers and their dependencies
        all_required_graphs = required_graphs.union(all_dependencies)

        # Get a topological sort of the subgraph containing only required graphs
        subgraph = self.dependency_graph.subgraph(all_required_graphs)
        execution_order = list(nx.topological_sort(subgraph))

        return execution_order

    def identify_required_inputs(self, execution_graphs: List[str]) -> Set[str]:
        """
        Identify all external inputs required by the execution graphs

        Args:
            execution_graphs: List of graph names to be executed

        Returns:
            Set of input names required from external sources
        """
        # Collect all inputs required by these graphs
        all_required_inputs = set()
        for graph_name in execution_graphs:
            graph_node = self.graphs[graph_name]
            all_required_inputs.update(graph_node.requires)

        # Remove inputs that are produced by other graphs in the execution list
        produced_outputs = set()
        for graph_name in execution_graphs:
            graph_node = self.graphs[graph_name]
            produced_outputs.update(graph_node.produces)

        # External inputs are those not produced internally
        external_inputs = all_required_inputs - produced_outputs

        return external_inputs


class ToolKit:
    def __init__(self):
        """Initialize the main controller for the output-driven system"""
        self.dependency_manager = DependencyManager()
        self.graph_builder = None
        self.compiled_graph = None

    def register_graphs(self, graphs: List[GraphNode]) -> None:
        """
        Register all graphs with the system

        Args:
            graphs: List of graph nodes to register
        """
        for graph in graphs:
            self.dependency_manager.register_graph(graph)

        # Build dependency edges after all graphs are registered
        self.dependency_manager.build_dependency_edges()

        # Verify no circular dependencies
        self.dependency_manager.check_circular_dependencies()
        
    def get_all_input_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all input fields from all registered graphs with their types and descriptions
        
        Returns:
            Dictionary mapping input_name -> {
                'type': type hint string,
                'description': description string,
                'required': whether this input is required by any graph,
                'used_by': list of graph names that use this input
            }
        """
        all_inputs = {}
        
        for graph_name, graph_node in self.dependency_manager.graphs.items():
            # Process required inputs
            for input_name in graph_node.requires:
                if input_name not in all_inputs:
                    all_inputs[input_name] = {
                        'type': graph_node.input_types.get(input_name, 'Any'),
                        'description': graph_node.input_descriptions.get(input_name, ''),
                        'required': True,
                        'used_by': [graph_name]
                    }
                else:
                    all_inputs[input_name]['used_by'].append(graph_name)
                    # If any graph requires it, mark as required
                    all_inputs[input_name]['required'] = True
            
            # Process optional inputs
            for input_name in graph_node.optional_inputs:
                if input_name not in all_inputs:
                    all_inputs[input_name] = {
                        'type': graph_node.input_types.get(input_name, 'Any'),
                        'description': graph_node.input_descriptions.get(input_name, ''),
                        'required': False,
                        'used_by': [graph_name]
                    }
                else:
                    all_inputs[input_name]['used_by'].append(graph_name)
        
        return all_inputs
    
    def get_all_output_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all output fields from all registered graphs with their types and descriptions
        
        Returns:
            Dictionary mapping output_name -> {
                'type': type hint string,
                'description': description string,
                'produced_by': name of the graph that produces this output
            }
        """
        all_outputs = {}
        
        for graph_name, graph_node in self.dependency_manager.graphs.items():
            for output_name in graph_node.produces:
                all_outputs[output_name] = {
                    'type': graph_node.output_types.get(output_name, 'Any'),
                    'description': graph_node.output_descriptions.get(output_name, ''),
                    'produced_by': graph_name
                }
        
        return all_outputs
    
    def print_schema(self) -> None:
        """
        Print a human-readable schema of all inputs and outputs in the system
        """
        inputs = self.get_all_input_fields()
        outputs = self.get_all_output_fields()
        
        print("=== INPUT SCHEMA ===")
        for name, info in inputs.items():
            req_status = "REQUIRED" if info['required'] else "OPTIONAL"
            print(f"{name} ({info['type']}) [{req_status}]")
            if info['description']:
                print(f"  Description: {info['description']}")
            print(f"  Used by: {', '.join(info['used_by'])}")
            print()
        
        print("\n=== OUTPUT SCHEMA ===")
        for name, info in outputs.items():
            print(f"{name} ({info['type']})")
            if info['description']:
                print(f"  Description: {info['description']}")
            print(f"  Produced by: {info['produced_by']}")
            print()

    def collect_inputs(self, required_inputs: Set[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Collect all required external inputs

        Args:
            required_inputs: Set of input names to collect
            context: Optional context with pre-filled inputs

        Returns:
            Dictionary of input_name -> input_value
        """
        input_values = context.copy() if context else {}

        # In a real implementation, this might prompt the user or call APIs to get missing inputs
        missing_inputs = required_inputs - set(input_values.keys())
        if missing_inputs:
            raise ValueError(f"Missing required inputs: {missing_inputs}")

        # Filter out only the inputs we need
        return {k: v for k, v in input_values.items() if k in required_inputs}

    def _build_langgraph(self, execution_order: List[str]) -> None:
        """
        Build a LangGraph StateGraph from the execution order
        
        Args:
            execution_order: List of node names in execution order
        """
        self.graph_builder = StateGraph(GraphState)
        
        # Add all nodes to the graph
        for node_name in execution_order:
            node = self.dependency_manager.graphs[node_name]
            
            # Define the node function
            def create_node_function(node_obj):
                def node_function(state: GraphState) -> Dict[str, Any]:
                    # Extract inputs needed by this node
                    node_inputs = {}
                    for input_name in node_obj.requires:
                        if input_name in state["inputs"]:
                            node_inputs[input_name] = state["inputs"][input_name]
                        elif input_name in state["outputs"]:
                            node_inputs[input_name] = state["outputs"][input_name]
                        else:
                            raise ValueError(f"Required input '{input_name}' not found for node '{node_obj.name}'")
                    
                    # Add optional inputs if available
                    for input_name in node_obj.optional_inputs:
                        if input_name in state["inputs"]:
                            node_inputs[input_name] = state["inputs"][input_name]
                        elif input_name in state["outputs"]:
                            node_inputs[input_name] = state["outputs"][input_name]
                    
                    # Execute the node's process function
                    node_outputs = node_obj.process_func(node_inputs)
                    
                    # Update the state with new outputs
                    updated_outputs = state["outputs"].copy()
                    updated_outputs.update(node_outputs)
                    
                    # Update execution order
                    updated_execution_order = state["execution_order"].copy()
                    updated_execution_order.append(node_obj.name)
                    
                    # Return the updates to the state
                    return {
                        "outputs": updated_outputs,
                        "execution_order": updated_execution_order
                    }
                
                return node_function
            
            # Add the node to the graph
            self.graph_builder.add_node(node.name, create_node_function(node))
        
        # Add edges between nodes based on the execution order
        for i in range(len(execution_order) - 1):
            self.graph_builder.add_edge(execution_order[i], execution_order[i + 1])
        
        # Set the entry point to the first node in the execution order
        if execution_order:
            self.graph_builder.set_entry_point(execution_order[0])
        
        # Compile the graph
        self.compiled_graph = self.graph_builder.compile()

    def process(self, desired_outputs: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point - start with desired outputs and work backwards

        Args:
            desired_outputs: List of output names the user wants
            context: Optional dictionary containing input values and context

        Returns:
            Dictionary of output_name -> output_value for requested outputs
        """
        # Determine execution order
        try:
            execution_order = self.dependency_manager.resolve_dependencies(desired_outputs)
        except ValueError as e:
            print(f"Error resolving dependencies: {e}")
            return {}

        # Identify required inputs
        required_inputs = self.dependency_manager.identify_required_inputs(execution_order)

        # Collect inputs
        try:
            input_values = self.collect_inputs(required_inputs, context)
        except ValueError as e:
            print(f"Error collecting inputs: {e}")
            return {}
            
        # Build the LangGraph
        self._build_langgraph(execution_order)
        
        if not self.compiled_graph:
            print("Failed to build graph")
            return {}
            
        # Initialize the state
        initial_state = {
            "inputs": input_values,
            "outputs": {},
            "execution_order": []
        }
        
        # Execute the graph
        try:
            final_state = self.compiled_graph.invoke(initial_state)
            
            # Extract and return only the requested outputs
            return {k: final_state["outputs"][k] for k in desired_outputs if k in final_state["outputs"]}
        except Exception as e:
            print(f"Error executing graph: {e}")
            return {}


# ---

# Create specific LangGraph implementations for different document processing tasks

def build_text_extraction_graph():
    """Build a LangGraph for extracting raw text from documents"""
    # This would use a real LangGraph implementation
    # For demonstration, we'll use a simple function

    def process_func(inputs):
        """Extract text from documents"""
        document = inputs["document"]
        print("Extracting text from document...")

        # Simulate text extraction
        text = f"This is the extracted text from {document['filename']}"

        return {
            "extracted_text": text,
            "document_metadata": {
                "filename": document["filename"],
                "page_count": len(document.get("content", "")) // 1000 + 1
            }
        }

    return process_func

def build_entity_extraction_graph():
    """Build a LangGraph for extracting entities from text"""

    def process_func(inputs):
        """Extract entities from text"""
        text = inputs["extracted_text"]
        print("Extracting entities from text...")

        # Simulate entity extraction with an LLM
        entities = {
            "people": ["John Doe", "Jane Smith"],
            "organizations": ["Acme Corp", "TechStartup Inc."],
            "locations": ["New York", "San Francisco"]
        }

        return {
            "entities": entities
        }

    return process_func

def build_sentiment_analysis_graph():
    """Build a LangGraph for analyzing sentiment"""

    def process_func(inputs):
        """Analyze sentiment from text"""
        text = inputs["extracted_text"]
        print("Analyzing sentiment...")

        # Simulate sentiment analysis
        sentiment = {
            "overall": "positive",
            "score": 0.75,
            "highlights": ["excellent service", "great product"]
        }

        return {
            "sentiment_analysis": sentiment
        }

    return process_func

def build_relationship_extraction_graph():
    """Build a LangGraph for extracting relationships between entities"""

    def process_func(inputs):
        """Extract relationships between entities"""
        entities = inputs["entities"]
        text = inputs["extracted_text"]
        print("Extracting relationships between entities...")

        # Simulate relationship extraction
        relationships = [
            {"source": "John Doe", "relationship": "works at", "target": "Acme Corp"},
            {"source": "Jane Smith", "relationship": "located in", "target": "New York"}
        ]

        return {
            "entity_relationships": relationships
        }

    return process_func

def build_summary_graph():
    """Build a LangGraph for generating document summaries"""

    def process_func(inputs):
        """Generate a summary of the document"""
        text = inputs["extracted_text"]
        entities = inputs.get("entities", None)  # Optional input
        sentiment = inputs.get("sentiment_analysis", None)  # Optional input

        print("Generating document summary...")

        # Generate different summaries based on available inputs
        if entities and sentiment:
            summary = f"Complete summary with entities and sentiment analysis"
        elif entities:
            summary = f"Summary with entity information but no sentiment"
        else:
            summary = f"Basic summary without entity or sentiment information"

        return {
            "document_summary": summary
        }

    return process_func

def build_report_generation_graph():
    """Build a LangGraph for generating final reports"""

    def process_func(inputs):
        """Generate a comprehensive report"""
        summary = inputs["document_summary"]
        relationships = inputs.get("entity_relationships", None)
        metadata = inputs["document_metadata"]

        print("Generating final report...")

        # Generate report based on available inputs
        if relationships:
            report = f"Comprehensive report with entity relationships"
        else:
            report = f"Basic report without relationship information"

        return {
            "final_report": report,
            "report_metadata": {
                "generated_at": "2023-04-01T12:00:00Z",
                "source_document": metadata["filename"]
            }
        }

    return process_func

# ---

def setup_document_processing_system():
    """Set up the complete document processing system"""
    # Initialize the ToolKit system
    system = ToolKit()

    # Create graph nodes for each processing step

    # 1. Text Extraction (starting point)
    text_extraction = GraphNode("text_extraction", build_text_extraction_graph())
    text_extraction.produces = ["extracted_text", "document_metadata"]
    text_extraction.requires = ["document"]
    text_extraction.add_input("document", required=True, type_hint="Dict[str, Any]", description="Input document")
    text_extraction.add_output("extracted_text", type_hint="str", description="Extracted text from the document")
    text_extraction.add_output("document_metadata", type_hint="Dict[str, Any]", description="Metadata about the document")

    # 2. Entity Extraction (depends on text extraction)
    entity_extraction = GraphNode("entity_extraction", build_entity_extraction_graph())
    entity_extraction.produces = ["entities"]
    entity_extraction.requires = ["extracted_text"]
    entity_extraction.add_input("extracted_text", required=True, type_hint="str", description="Text to extract entities from")
    entity_extraction.add_output("entities", type_hint="Dict[str, List[str]]", description="Extracted entities")

    # 3. Sentiment Analysis (depends on text extraction)
    sentiment_analysis = GraphNode("sentiment_analysis", build_sentiment_analysis_graph())
    sentiment_analysis.produces = ["sentiment_analysis"]
    sentiment_analysis.requires = ["extracted_text"]
    sentiment_analysis.add_input("extracted_text", required=True, type_hint="str", description="Text to analyze sentiment")
    sentiment_analysis.add_output("sentiment_analysis", type_hint="Dict[str, Any]", description="Sentiment analysis results")

    # 4. Relationship Extraction (depends on entity extraction)
    relationship_extraction = GraphNode("relationship_extraction", build_relationship_extraction_graph())
    relationship_extraction.produces = ["entity_relationships"]
    relationship_extraction.requires = ["entities", "extracted_text"]
    relationship_extraction.add_input("entities", required=True, type_hint="Dict[str, List[str]]", description="Entities to extract relationships")
    relationship_extraction.add_input("extracted_text", required=True, type_hint="str", description="Text to extract relationships from")
    relationship_extraction.add_output("entity_relationships", type_hint="List[Dict[str, str]]", description="Extracted entity relationships")

    # 5. Summary Generation (depends on text extraction, optionally uses entities and sentiment)
    summary_generation = GraphNode("summary_generation", build_summary_graph())
    summary_generation.produces = ["document_summary"]
    summary_generation.requires = ["extracted_text"]
    summary_generation.optional_inputs = ["entities", "sentiment_analysis"]
    summary_generation.add_input("extracted_text", required=True, type_hint="str", description="Text to generate summary")
    summary_generation.add_input("entities", required=False, type_hint="Dict[str, List[str]]", description="Entities to include in summary")
    summary_generation.add_input("sentiment_analysis", required=False, type_hint="Dict[str, Any]", description="Sentiment analysis to include in summary")
    summary_generation.add_output("document_summary", type_hint="str", description="Generated document summary")

    # 6. Report Generation (depends on summary and metadata, optionally uses relationships)
    report_generation = GraphNode("report_generation", build_report_generation_graph())
    report_generation.produces = ["final_report", "report_metadata"]
    report_generation.requires = ["document_summary", "document_metadata"]
    report_generation.optional_inputs = ["entity_relationships"]
    report_generation.add_input("document_summary", required=True, type_hint="str", description="Summary to include in report")
    report_generation.add_input("document_metadata", required=True, type_hint="Dict[str, Any]", description="Metadata to include in report")
    report_generation.add_input("entity_relationships", required=False, type_hint="List[Dict[str, str]]", description="Entity relationships to include in report")
    report_generation.add_output("final_report", type_hint="str", description="Generated final report")
    report_generation.add_output("report_metadata", type_hint="Dict[str, Any]", description="Metadata about the generated report")

    # Register all graphs with the system
    system.register_graphs([
        text_extraction,
        entity_extraction,
        sentiment_analysis,
        relationship_extraction,
        summary_generation,
        report_generation
    ])

    return system

# ---

def document_processing_example():
    """Run a complete example of the document processing system"""
    # Set up the system
    system = setup_document_processing_system()

    # Create a visualization of the dependency graph
    import matplotlib.pyplot as plt

    dependency_graph = system.dependency_manager.dependency_graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(dependency_graph)
    nx.draw(dependency_graph, pos, with_labels=True, node_size=2000, node_color="lightblue",
            font_size=10, font_weight="bold", arrows=True, arrowsize=15)
    plt.title("Graph Dependency Network")
    plt.savefig("graph_dependencies.png")
    print("Saved dependency visualization to 'graph_dependencies.png'")

    # Sample document input
    sample_document = {
        "filename": "business_proposal.pdf",
        "content": "This is a sample document content..." * 10
    }

    # Example 1: Request just a basic summary
    print("\n=== Example 1: Basic Summary ===")
    desired_outputs_1 = ["document_summary"]
    result_1 = system.process(
        desired_outputs=desired_outputs_1,
        context={"document": sample_document}
    )

    print("\nResults:")
    for output_name, output_value in result_1.items():
        print(f"{output_name}: {output_value}")

    # Example 2: Request a complete report with entity relationships
    print("\n=== Example 2: Complete Report with Relationships ===")
    desired_outputs_2 = ["final_report", "entity_relationships"]
    result_2 = system.process(
        desired_outputs=desired_outputs_2,
        context={"document": sample_document}
    )

    print("\nResults:")
    for output_name, output_value in result_2.items():
        print(f"{output_name}: {output_value}")

    # Example 3: Request just entities and sentiment
    print("\n=== Example 3: Entities and Sentiment ===")
    desired_outputs_3 = ["entities", "sentiment_analysis"]
    result_3 = system.process(
        desired_outputs=desired_outputs_3,
        context={"document": sample_document}
    )

    print("\nResults:")
    for output_name, output_value in result_3.items():
        print(f"{output_name}: {output_value}")

    # Example 4: Visualize the execution paths for different output requests
    print("\n=== Example 4: Execution Path Visualization ===")

    def visualize_execution_path(desired_outputs):
        execution_order = system.dependency_manager.resolve_dependencies(desired_outputs)
        print(f"To produce {desired_outputs}, execution order is: {execution_order}")

        # Draw subgraph of just the required nodes
        subgraph = dependency_graph.subgraph(execution_order)
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(subgraph)
        nx.draw(subgraph, pos, with_labels=True, node_size=2000, node_color="lightgreen",
                font_size=10, font_weight="bold", arrows=True, arrowsize=15)

        # Add output labels at the bottom of the visualization
        for i, output in enumerate(desired_outputs):
            plt.text(0.5, 0.1 + i*0.1, f"Output: {output}",
                    transform=plt.gca().transAxes, fontsize=12)

        plt.title(f"Execution Path for: {', '.join(desired_outputs)}")
        plt.savefig(f"execution_path_{'_'.join(desired_outputs)}.png")
        print(f"Saved execution path visualization to 'execution_path_{'_'.join(desired_outputs)}.png'")

    visualize_execution_path(["document_summary"])
    visualize_execution_path(["final_report"])
    visualize_execution_path(["entities", "sentiment_analysis"])

    # Print schema
    print("\n=== INPUT/OUTPUT SCHEMA ===")
    system.print_schema()

# Run the example
if __name__ == "__main__":
    document_processing_example()
