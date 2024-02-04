import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;
import java.io.IOException;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

import javax.swing.ButtonGroup;
import javax.swing.DefaultComboBoxModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JRadioButton;
import javax.swing.JTextField;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.formdev.flatlaf.FlatDarculaLaf;


////////////////////////////////////////////////////////////////////////////////-----------Fenetre TRINING------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class Training extends JFrame {
	

	private static final long serialVersionUID = 1L;
	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	
	private JButton btn1;
	private JButton btn2;
	private JTextField textFieldNE;
	private JTextField textFieldBS;
	private JTextField textFieldNL;
	private JTextField HybMLPtextFieldNE;
	private JTextField HybMLPtextFieldNL;
	private JTextField HybMLPtextFieldBS;
	private JTextField textFieldP;
	private JTextField textFieldPath;
	private JFileChooser fileChooser;
	private String Folder_Selected;
	
	
	
	private JComboBox<String> HybMLPcomboBoxES ;
	private JComboBox<String> comboBoxES;
	private JComboBox<String> HybMLPcomboBoxPF;
	private JComboBox<String> comboBoxOPT;
	private JComboBox<String> comboBoxPF ;
	private JComboBox<String> HybMLPcomboBoxOPT;
	private JButton btnchooser;
	private JRadioButton RadiobtnMLP ;
	private JRadioButton RadiobtnHybMLP; 
	private String Path_save;
	private Boolean model_created=false;
	private String C_model;
	
	

	/**
	 * Launch the application.
	 * @throws UnsupportedLookAndFeelException 
	 */
	public static void main(String[] args) throws UnsupportedLookAndFeelException {
		FlatDarculaLaf.install();	
		UIManager.setLookAndFeel(new FlatDarculaLaf() );
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Training frame = new Training("2","C:/Users/name/Desktop/...",true);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	

	/**
	 * Create the frame.
	 */
	public Training(String dataset,String path_data,Boolean DataProcessed) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(Training.class.getResource("/Menu_img/train.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);

		setTitle("Trainig");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(0, 0, 1100, 650);
		setShape(new RoundRectangle2D.Double(0d, 0d, 1100d, 650d, 25d, 25d));
		setLocationRelativeTo(null);
		//vu que la frame est Undecorated on a besoin de ces MouseListeners pour la faire bouger(frame)
		  addMouseListener(new MouseAdapter() {
	            @Override
	            //on recupere les coordonnées de la souris
	            public void mousePressed(MouseEvent e) {
	                posX = e.getX();    //Position X de la souris au clic
	                posY = e.getY();    //Position Y de la souris au clic
	            }
	        });
	        addMouseMotionListener(new MouseMotionAdapter() {
	            // A chaque deplacement on recalcul le positionnement de la fenetre
	            @Override
	            public void mouseDragged(MouseEvent e) {
	                int depX = e.getX() - posX;
	                int depY = e.getY() - posY;
	                setLocation(getX()+depX, getY()+depY);
	            }
	        });
	        
	        
		contentPane = new JPanel();
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel BGDatasets = new JLabel("");
		if(!dataset.equals("3") && !dataset.equals("0"))
			BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/1.png")));
		else BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/1'.png")));
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Training.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(Training.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(Training.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				JButton btnHome = new JButton("");
				btnHome.addMouseListener(new MouseAdapter() {
					@Override
					public void mouseEntered(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(Training.class.getResource("/Models_img/home selected.png")));//changer les couleurs button
						}
					}
					@Override
					public void mouseExited(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(Training.class.getResource("/Models_img/home.png")));//remetre le bouton de base
						}
					}
				});
				btnHome.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						String Path_save =textFieldPath.getText();
						Menu frame = new Menu(String.valueOf(dataset),Path_save,DataProcessed);// retourner au menu medecin
							frame.setLocationRelativeTo(null);
							frame.setVisible(true);
							dispose();
					}
				});
				btnHome.setIcon(new ImageIcon(Training.class.getResource("/Models_img/home.png")));
				btnHome.setToolTipText("Menu");
				btnHome.setBounds(974, 11, 32, 32);
				ButtonStyle(btnHome);
				contentPane.add(btnHome);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Training.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(Training.class.getResource("/Menu_img/Exit ML.png")));
			}
		});
		Exit_BTN.setToolTipText("Exit");
		ButtonStyle(Exit_BTN);
		Exit_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			
					
					int ClickedButton	=JOptionPane.showConfirmDialog(null, "Do you really want to leave?", "Close", JOptionPane.YES_NO_OPTION);
					if(ClickedButton==JOptionPane.YES_OPTION)
					{					
						dispose();
					}
					
					
			}
			
		});
		Exit_BTN.setIcon(new ImageIcon(Training.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
//btns ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		btn1= new JButton("");
		btn1.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
					if(!dataset.equals("3") && !dataset.equals("0"))
						BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/2.png")));
					else BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/2'.png")));
					
			}
			@Override
			public void mouseExited(MouseEvent e) {
					if(!dataset.equals("3") && !dataset.equals("0"))
						BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/1.png")));
					else BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/1'.png")));
			}
		});
		btn1.setToolTipText("Start training");
		btn1.setForeground(Color.WHITE);
		btn1.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
		btn1.addActionListener(new ActionListener() {
			Process process;
			Boolean stopped = false;
			public void actionPerformed(ActionEvent arg0) {
				
				if (!RadiobtnMLP.isSelected() && !RadiobtnHybMLP.isSelected()) {
					JOptionPane.showMessageDialog(null, "Please select a model to tain.");
				}
				else {
				
				  JFrame f = new JFrame("Stepping Progress");
				    f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				    
				    f.setUndecorated(true);	
				    f.setResizable(false);
				    f.setSize(600, 200);
				    f.setShape(new RoundRectangle2D.Double(0d, 0d, 600, 200, 25d, 25d));
				    
				    f.setLocationRelativeTo(null);
				    
				    
				    final JProgressBar aJProgressBar = new JProgressBar();
				    aJProgressBar.setBounds(110,92,400, 16);;
				    aJProgressBar.setIndeterminate(true);
				    f.getContentPane().add(aJProgressBar);
				 
					final CyclicBarrier gate = new CyclicBarrier(3);
					
					Thread t1 = new Thread(){
					    public void run(){
					        try {
								gate.await();
							} catch (InterruptedException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							} catch (BrokenBarrierException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}	
				
				
										String early_stopping;
										String epochs;
										String optimizer_subs;
										String emb_size_mlp;
										String emb_size_Hybmlp;
										String pred_facts;
										String num_layers;
										String model_to_train;
										String batch ;
										String dataset_= dataset;
										String path_data_ = path_data;
										
										
										if (RadiobtnMLP.isSelected()) {
											C_model="2";
											//MLP
											Path_save=textFieldPath.getText();
											// String dataset  =textFieldPath.getText(); de la fenetre dataset
											model_to_train = "2";
											epochs =textFieldNE.getText();
											optimizer_subs  =(String) comboBoxOPT.getSelectedItem();
											emb_size_mlp =(String) comboBoxES.getSelectedItem();
											pred_facts =(String) comboBoxPF.getSelectedItem();
											num_layers =textFieldNL.getText();
											early_stopping = textFieldP.getText();
											if (early_stopping.equals("1 , 2 ...")) {
												 early_stopping="-1";
											}
											// String path_data  =textFieldPath.getText();de la fenetre dataset
											batch  =textFieldBS.getText();		
											
											if (epochs.equals("1 , 2 ...")) {
												epochs="5";
											}
											if (optimizer_subs.equals("Choose")) {
												optimizer_subs="adam";
											}
											if (emb_size_mlp.equals("Choose")) {
												emb_size_mlp="32";
											}
											if (pred_facts.equals("Choose")) {
												pred_facts="16";
											}
											if (num_layers.equals("1 , 2 ...")) {
												num_layers="5";
											}
											if (batch.equals("1 , 2 ...")) {
												batch="100";
											}
											if (dataset.equals("0")) {
												dataset_="3";
											}
											if (path_data.equals("C:/Users/name/Desktop/...")) {
												path_data_="C:/users/" + System.getProperty("user.name") + "/Desktop/";
											}
											else {
												path_data_ =path_data+'\\';
											}
											if (Path_save.equals("C:/Users/name/Desktop/...")) {
												Path_save="C:/users/" + System.getProperty("user.name") + "/Desktop/";
											}
											else {
												 Path_save =textFieldPath.getText()+'\\';
											}
											
											
						
											String path_script ="";
											path_script = test.class.getResource("/scripts_py/Modules.py").getPath(); // get the path of the script (a revoir)
											path_script = path_script.substring(1, path_script.length());
											
											model_created=true;
											
											ProcessBuilder pb = new ProcessBuilder("python",path_script,"--path_save",Path_save,
													"--model",model_to_train,"--epochs",epochs,"--optimizer_subs",optimizer_subs,"--batch_size",batch,"--num_layers",num_layers,
													"--emb_size_mlp",emb_size_mlp,"--num_factors",pred_facts,"--estop",early_stopping,"--path_data",path_data_,"--dataset",dataset_).inheritIO();
											try {
											 process=pb.start();
												try {
													 process.waitFor();
												} catch (InterruptedException e1) {
													// TODO Auto-generated catch block
													e1.printStackTrace();
												}
											} catch (IOException e) {
												// TODO Auto-generated catch block
												JOptionPane.showMessageDialog(null,e);
											}	
						
										}
										if (RadiobtnHybMLP.isSelected()) {
											C_model="1";
											model_to_train = "1";
											//MLP
											Path_save=textFieldPath.getText();
											// String dataset  =textFieldPath.getText(); de la fenetre dataset
											model_to_train = "1";
											epochs =HybMLPtextFieldNE.getText();
											optimizer_subs  =(String) HybMLPcomboBoxOPT.getSelectedItem();
											emb_size_Hybmlp =(String) HybMLPcomboBoxES.getSelectedItem();
											pred_facts =(String) HybMLPcomboBoxPF.getSelectedItem();
											num_layers =HybMLPtextFieldNL.getText();
											early_stopping = textFieldP.getText();
											if (early_stopping.equals("1 , 2 ...")) {
												 early_stopping="-1";
											}
											// String path_data  =textFieldPath.getText();de la fenetre dataset
											batch  =HybMLPtextFieldBS.getText();
											
											if (epochs.equals("1 , 2 ...")) {
												epochs="5";
											}
											if (optimizer_subs.equals("Choose")) {
												optimizer_subs="adam";
											}
											if (emb_size_Hybmlp.equals("Choose")) {
												emb_size_Hybmlp="32";
											}
											if (pred_facts.equals("Choose")) {
												pred_facts="16";
											}
											if (num_layers.equals("1 , 2 ...")) {
												num_layers="5";
											}
											if (batch.equals("1 , 2 ...")) {
												batch="100";
											}
											if (dataset.equals("0")) {
												dataset_="3";
											}
											if (path_data.equals("C:/Users/name/Desktop/...")) {
												path_data_="C:/users/" + System.getProperty("user.name") + "/Desktop/";
											}
											else {
												path_data_ =path_data+'\\';
											}
											if (Path_save.equals("C:/Users/name/Desktop/...")) {
												Path_save="C:/users/" + System.getProperty("user.name") + "/Desktop/";
											}
											else {
												 Path_save =textFieldPath.getText()+'\\';
											}
						
											String path_script ="";
											path_script = test.class.getResource("/scripts_py/Modules.py").getPath(); // get the path of the script (a revoir)
											path_script = path_script.substring(1, path_script.length());
											
											model_created=true;
											
											ProcessBuilder pb = new ProcessBuilder("python",path_script,"--path_save",Path_save,
													"--model",model_to_train,"--epochs",epochs,"--optimizer_subs",optimizer_subs,"--batch_size",batch,"--num_layers",num_layers,
													"--emb_size_hybmlp",emb_size_Hybmlp,"--num_factors",pred_facts,"--estop",early_stopping,"--path_data",path_data_,"--dataset",dataset_).inheritIO();
											try {
												process=pb.start();
												try {
													 process.waitFor();
												} catch (InterruptedException e1) {
													// TODO Auto-generated catch block
													e1.printStackTrace();
												}
											} catch (IOException e) {
												// TODO Auto-generated catch block
												JOptionPane.showMessageDialog(null,e);
											}
						
										}
										
										if(!stopped) {
											f.dispose();
											JOptionPane.showMessageDialog(null,  "Completed Training !","state" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/stamp.png")));	
											/*String path_res = test.class.getResource("/scripts_py/P-r-e-s/result.png").getPath();
											File file = new File(path_res);
									        
									        //first check if Desktop is supported by Platform or not
									        if(!Desktop.isDesktopSupported()){
									            return;
									        }
									        
									        Desktop desktop = Desktop.getDesktop();
									        if(file.exists())
												try {
													desktop.open(file);
												} catch (IOException e) {
													// TODO Auto-generated catch block
													e.printStackTrace();
												} */   
										}
						                else {
						                	f.dispose();
											JOptionPane.showMessageDialog(null,  "Stopped Training.","state" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	
											stopped=false;
						                }
										
				
					    }};
					    
				Thread t2 = new Thread(){
				    public void run(){
				        try {
							gate.await();
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						} catch (BrokenBarrierException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
				        
				        JButton btnStop = new JButton("Stop");
				        btnStop.addMouseListener(new MouseAdapter() {
							@Override
							public void mouseClicked(MouseEvent e) {
								stopped=true;
								process.destroy();
							}
						});
				        btnStop.setToolTipText("Stop processing");
				        btnStop.setBounds(250, 130, 100, 25);
						f.getContentPane().add(btnStop);
						
						JLabel BG = new JLabel("");
						BG.setIcon(new ImageIcon(Datasets.class.getResource("/Training_img/process Train.png")));
						BG.setBounds(0, 0, 600, 200);
						f.getContentPane().add(BG);

					    f.setVisible(true);  
				    }};

				t1.start();
				t2.start();

				// At this point, t1 and t2 are blocking on the gate. 
				// Since we gave "3" as the argument, gate is not opened yet.
				// Now if we block on the gate from the main thread, it will open
				// and all threads will start to do stuff!

				try {
					gate.await();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (BrokenBarrierException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}    
			    
				
				
				}
			}
		});
		btn1.setBounds(782, 395, 215, 44);
		ButtonStyle(btn1);
		contentPane.add(btn1);
		
		btn2= new JButton("");
		btn2.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				if(!dataset.equals("3") && !dataset.equals("0"))
					BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/3.png")));
				else BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/3'.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
					if(!dataset.equals("3") && !dataset.equals("0"))
						BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/1.png")));
					else BGDatasets.setIcon(new ImageIcon(Training.class.getResource("/Training_img/1'.png")));
			}
		});
		btn2.setToolTipText("Next");
		btn2.setForeground(Color.WHITE);
		btn2.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
		btn2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				if (model_created) {
					if (dataset.equals("0")) {
						predict frame = new predict("3",path_data,Path_save,DataProcessed,C_model);
						frame.setLocationRelativeTo(null);
						frame.setVisible(true);
						dispose();
					}
					else {
						predict frame = new predict(dataset,path_data,Path_save,DataProcessed,C_model);
						frame.setLocationRelativeTo(null);
						frame.setVisible(true);
						dispose();
						
					}
				}
				else
				JOptionPane.showMessageDialog(null,  "Please creat and train a model.","Warning" ,JOptionPane.PLAIN_MESSAGE, new ImageIcon(Datasets.class.getResource("/state/error.png")));	

			}
		});
		btn2.setBounds(782, 530, 220, 44);
		ButtonStyle(btn2);
		contentPane.add(btn2);
//radio btns//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////	
		RadiobtnMLP = new JRadioButton("");
		RadiobtnMLP.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (RadiobtnMLP.isSelected()) {
					//NEUTRE
					textFieldPath.setEnabled(true);
					btnchooser.setEnabled(true);
					btn1.setEnabled(true);
					btn2.setEnabled(true);
					textFieldP.setEnabled(true);
					//MLP
					textFieldNE.setEnabled(true);
					textFieldBS.setEnabled(true);
					textFieldNL.setEnabled(true); 
					comboBoxOPT.setEnabled(true);
					comboBoxPF.setEnabled(true);
					comboBoxES.setEnabled(true);
					//HybMLP
					HybMLPtextFieldNE.setEnabled(false);
					HybMLPtextFieldBS.setEnabled(false);
					HybMLPtextFieldNL.setEnabled(false); 
					HybMLPcomboBoxOPT.setEnabled(false);
					HybMLPcomboBoxPF.setEnabled(false);
					HybMLPcomboBoxES.setEnabled(false);
				}
			}
		});
		RadiobtnMLP.setToolTipText("MLP");
		RadiobtnMLP.setBounds(118, 80, 21, 23);
		contentPane.add(RadiobtnMLP);
		
		RadiobtnHybMLP = new JRadioButton("");
		RadiobtnHybMLP.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				//NEUTRE
				textFieldPath.setEnabled(true);
				textFieldP.setEnabled(true);
				btnchooser.setEnabled(true);
				btn1.setEnabled(true);
				btn2.setEnabled(true);
				//MLP
				textFieldNE.setEnabled(false);
				textFieldBS.setEnabled(false);
				textFieldNL.setEnabled(false); 
				comboBoxOPT.setEnabled(false);
				comboBoxPF.setEnabled(false);
				comboBoxES.setEnabled(false);
				//HybMLP
				HybMLPtextFieldNE.setEnabled(true);
				HybMLPtextFieldBS.setEnabled(true);
				HybMLPtextFieldNL.setEnabled(true); 
				HybMLPcomboBoxOPT.setEnabled(true);
				HybMLPcomboBoxPF.setEnabled(true);
				HybMLPcomboBoxES.setEnabled(true);
			}
		});
		RadiobtnHybMLP.setToolTipText("HybMLP");
		RadiobtnHybMLP.setBounds(410, 80, 21, 23);
		contentPane.add(RadiobtnHybMLP);
		if(dataset.equals("3")) RadiobtnHybMLP.setEnabled(false);
		
		
		   //Group the radio buttons.
		ButtonGroup group = new ButtonGroup();
		group.add(RadiobtnMLP);
		group.add(RadiobtnHybMLP);
		
		textFieldNE = new JTextField();
		textFieldNE.setEnabled(false);
		textFieldNE.setToolTipText("MLP  Number of epochs");
		textFieldNE.setText("1 , 2 ...");
		textFieldNE.setForeground(Color.GRAY);
		textFieldNE.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldNE.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		textFieldNE.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldNE.getText().toString().equals("1 , 2 ...")) {
					textFieldNE.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldNE.setForeground(Color.LIGHT_GRAY);
					textFieldNE.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldNE.getText().toString().equals("")) {
					textFieldNE.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldNE.setForeground(Color.GRAY);
					textFieldNE.setText("1 , 2 ...");
				}
			}
		});
		textFieldNE.setColumns(10);
		textFieldNE.setBounds(283, 262, 78, 32);
		contentPane.add(textFieldNE);
		
		textFieldBS = new JTextField();
		textFieldBS.setEnabled(false);
		textFieldBS.setToolTipText("MLP Batch size");
		textFieldBS.setText("1 , 2 ...");
		textFieldBS.setForeground(Color.GRAY);
		textFieldBS.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldBS.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		textFieldBS.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldBS.getText().toString().equals("1 , 2 ...")) {
					textFieldBS.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldBS.setForeground(Color.LIGHT_GRAY);
					textFieldBS.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldBS.getText().toString().equals("")) {
					textFieldBS.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldBS.setForeground(Color.GRAY);
					textFieldBS.setText("1 , 2 ...");
				}
			}
		});
		textFieldBS.setColumns(10);
		textFieldBS.setBounds(240, 397, 78, 32);
		contentPane.add(textFieldBS);
		
		textFieldNL = new JTextField();
		textFieldNL.setEnabled(false);
		textFieldNL.setToolTipText("MLP Number of layers");
		textFieldNL.setText("1 , 2 ...");
		textFieldNL.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		textFieldNL.setForeground(Color.GRAY);
		textFieldNL.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldNL.getText().toString().equals("1 , 2 ...")) {
					textFieldNL.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldNL.setForeground(Color.LIGHT_GRAY);
					textFieldNL.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldNL.getText().toString().equals("")) {
					textFieldNL.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldNL.setForeground(Color.GRAY);
					textFieldNL.setText("1 , 2 ...");
				}
			}
		});
		textFieldNL.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldNL.setColumns(10);
		textFieldNL.setBounds(283, 353, 78, 32);
		contentPane.add(textFieldNL);
		
		comboBoxOPT = new JComboBox<String>();
		comboBoxOPT.setEnabled(false);
		comboBoxOPT.setToolTipText("MLP Optimizer");
		comboBoxOPT.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","SGD","Adam"} ));
		comboBoxOPT.setBounds(237, 216, 132, 32);
		contentPane.add(comboBoxOPT);
		
		comboBoxPF = new JComboBox<String>();
		comboBoxPF.setEnabled(false);
		comboBoxPF.setToolTipText("MLP Number of predictive factors");
		comboBoxPF.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","8","16","32","64","128"} ));
		comboBoxPF.setBounds(259, 308, 96, 32);
		contentPane.add(comboBoxPF);
		
		HybMLPcomboBoxOPT = new JComboBox<String>();
		HybMLPcomboBoxOPT.setEnabled(false);
		HybMLPcomboBoxOPT.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","SGD","Adam"} ));
		HybMLPcomboBoxOPT.setToolTipText("HybMLP Optimizer");
		HybMLPcomboBoxOPT.setBounds(559, 216, 132, 32);
		contentPane.add(HybMLPcomboBoxOPT);
		
		HybMLPtextFieldNE = new JTextField();
		HybMLPtextFieldNE.setEnabled(false);
		HybMLPtextFieldNE.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		HybMLPtextFieldNE.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (HybMLPtextFieldNE.getText().toString().equals("1 , 2 ...")) {
					HybMLPtextFieldNE.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					HybMLPtextFieldNE.setForeground(Color.LIGHT_GRAY);
					HybMLPtextFieldNE.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (HybMLPtextFieldNE.getText().toString().equals("")) {
					HybMLPtextFieldNE.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					HybMLPtextFieldNE.setForeground(Color.GRAY);
					HybMLPtextFieldNE.setText("1 , 2 ...");
				}
			}
		});
		HybMLPtextFieldNE.setToolTipText("HybMLP Number of epochs");
		HybMLPtextFieldNE.setText("1 , 2 ...");
		HybMLPtextFieldNE.setForeground(Color.GRAY);
		HybMLPtextFieldNE.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		HybMLPtextFieldNE.setColumns(10);
		HybMLPtextFieldNE.setBounds(609, 262, 78, 32);
		contentPane.add(HybMLPtextFieldNE);
		
		HybMLPcomboBoxPF = new JComboBox<String>();
		HybMLPcomboBoxPF.setEnabled(false);
		HybMLPcomboBoxPF.setToolTipText("HybMLP Number of predictive factors");
		HybMLPcomboBoxPF.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","8","16","32","64","128"} ));
		HybMLPcomboBoxPF.setBounds(583, 308, 96, 32);
		contentPane.add(HybMLPcomboBoxPF);
		
		HybMLPtextFieldNL = new JTextField();
		HybMLPtextFieldNL.setEnabled(false);
		HybMLPtextFieldNL.setToolTipText("HybMLP Number of layers");
		HybMLPtextFieldNL.setText("1 , 2 ...");
		HybMLPtextFieldNL.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		HybMLPtextFieldNL.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (HybMLPtextFieldNL.getText().toString().equals("1 , 2 ...")) {
					HybMLPtextFieldNL.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					HybMLPtextFieldNL.setForeground(Color.LIGHT_GRAY);
					HybMLPtextFieldNL.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (HybMLPtextFieldNL.getText().toString().equals("")) {
					HybMLPtextFieldNL.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					HybMLPtextFieldNL.setForeground(Color.GRAY);
					HybMLPtextFieldNL.setText("1 , 2 ...");
				}
			}
		});
		HybMLPtextFieldNL.setForeground(Color.GRAY);
		HybMLPtextFieldNL.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		HybMLPtextFieldNL.setColumns(10);
		HybMLPtextFieldNL.setBounds(609, 353, 78, 32);
		contentPane.add(HybMLPtextFieldNL);
		
		HybMLPtextFieldBS = new JTextField();
		HybMLPtextFieldBS.setEnabled(false);
		HybMLPtextFieldBS.setToolTipText("HybMLP Batch size");
		HybMLPtextFieldBS.setText("1 , 2 ...");
		HybMLPtextFieldBS.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		HybMLPtextFieldBS.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (HybMLPtextFieldBS.getText().toString().equals("1 , 2 ...")) {
					HybMLPtextFieldBS.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					HybMLPtextFieldBS.setForeground(Color.LIGHT_GRAY);
					HybMLPtextFieldBS.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (HybMLPtextFieldBS.getText().toString().equals("")) {
					HybMLPtextFieldBS.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					HybMLPtextFieldBS.setForeground(Color.GRAY);
					HybMLPtextFieldBS.setText("1 , 2 ...");
				}
			}
		});
		HybMLPtextFieldBS.setForeground(Color.GRAY);
		HybMLPtextFieldBS.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		HybMLPtextFieldBS.setColumns(10);
		HybMLPtextFieldBS.setBounds(559, 397, 78, 32);
		contentPane.add(HybMLPtextFieldBS);
		
		comboBoxES = new JComboBox<String>();
		comboBoxES.setEnabled(false);
		comboBoxES.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","8","16","32","64","128"} ));
		comboBoxES.setToolTipText("MLP Embedding size");
		comboBoxES.setBounds(259, 172, 96, 32);
		contentPane.add(comboBoxES);
		
		HybMLPcomboBoxES = new JComboBox<String>();
		HybMLPcomboBoxES.setEnabled(false);
		HybMLPcomboBoxES.setModel(new DefaultComboBoxModel<String>(new String[] {"Choose","8","16","32","64","128"} ));
		HybMLPcomboBoxES.setToolTipText("HybMLP Embedding size");
		HybMLPcomboBoxES.setBounds(583, 172, 96, 32);
		contentPane.add(HybMLPcomboBoxES);
		
		textFieldP = new JTextField();
		textFieldP.setEnabled(false);
		textFieldP.setToolTipText("Patience");
		textFieldP.addKeyListener(new KeyAdapter() {
		    public void keyTyped(KeyEvent e) {
		      char c = e.getKeyChar();
		      if (!((c >= '0') && (c <= '9') ||
		         (c == KeyEvent.VK_BACK_SPACE) ||
		         (c == KeyEvent.VK_DELETE))) {
		        getToolkit().beep();
		        e.consume();
		      }
		    }
		  });
		textFieldP.setText("1 , 2 ...");
		textFieldP.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldP.getText().toString().equals("1 , 2 ...")) {
					textFieldP.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldP.setForeground(Color.LIGHT_GRAY);
					textFieldP.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldP.getText().toString().equals("")) {
					textFieldP.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldP.setForeground(Color.GRAY);
					textFieldP.setText("1 , 2 ...");
				}
			}
		});
		textFieldP.setForeground(Color.GRAY);
		textFieldP.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 12));
		textFieldP.setColumns(10);
		textFieldP.setBounds(858, 188, 116, 32);
		contentPane.add(textFieldP);
//PATH TO SAVE MODEL/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////		
		textFieldPath = new JTextField();
		textFieldPath.setEnabled(false);
		textFieldPath.setEditable(false);
		textFieldPath.setToolTipText("Path to save train & test files");
		textFieldPath.setText("C:/Users/name/Desktop/...");
		textFieldPath.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
		textFieldPath.setForeground(Color.GRAY);
		textFieldPath.addFocusListener(new FocusAdapter() {
			@Override
			public void focusGained(FocusEvent e) {
				if (textFieldPath.getText().toString().equals("C:/Users/name/Desktop/...") && textFieldPath.isEditable()) {
					textFieldPath.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
					textFieldPath.setForeground(Color.LIGHT_GRAY);
					textFieldPath.setText("");
				}
			}
			@Override
			public void focusLost(FocusEvent e) {
				if (textFieldPath.getText().toString().equals("")) {
					textFieldPath.setFont(new Font("Microsoft PhagsPa",Font.CENTER_BASELINE,12));
					textFieldPath.setForeground(Color.GRAY);
					textFieldPath.setText("C:/Users/name/Desktop/...");
				}
			}
		});
		textFieldPath.setColumns(10);
		textFieldPath.setBounds(724, 327, 234, 34);
		contentPane.add(textFieldPath);
		
		btnchooser = new JButton("");
		btnchooser.setEnabled(false);
		btnchooser.setIcon(new ImageIcon(Datasets.class.getResource("/Datasets_img/folder.png")));
		btnchooser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				fileChooser = new JFileChooser(); 
				fileChooser.setDialogTitle("Choose Directory");
	            fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	            int option = fileChooser.showOpenDialog(btnchooser);
	            if(option == JFileChooser.APPROVE_OPTION){
	            	Folder_Selected = fileChooser.getSelectedFile().getAbsolutePath();
	            	textFieldPath.setText(Folder_Selected);
	            	textFieldPath.setForeground(Color.LIGHT_GRAY);
	            }else{
	            	Folder_Selected= "C:/Users/name/Desktop/...";
	            }
			}
		});
		btnchooser.setToolTipText("Path chooser");
		btnchooser.setBounds(968, 327, 34, 34);
		contentPane.add(btnchooser);
		
		
		JButton btnNewButton = new JButton("");
		btnNewButton.setToolTipText("GO to datasets");
		btnNewButton.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/previous selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnNewButton.setIcon(new ImageIcon(Datasets.class.getResource("/arrows/previous.png")));
			}
		});
		btnNewButton.setIcon(new ImageIcon(Training.class.getResource("/arrows/previous.png")));
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				Datasets frame = new Datasets(dataset,path_data,DataProcessed);
				frame.setLocationRelativeTo(contentPane);
				frame.setVisible(true);
				dispose();
			}
		});
		btnNewButton.setBounds(295, 87, 32, 32);
		ButtonStyle(btnNewButton);
		contentPane.add(btnNewButton);
		
		
//le background////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		BGDatasets.setBounds(0, 0, 1100, 650);
		contentPane.add(BGDatasets);
		
	}
//methode du style des buttons/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	 private void ButtonStyle(JButton btn) {
	//enlecer les bordures des btn
	 btn.setOpaque(false);
	 btn.setFocusPainted(false);
	 btn.setBorderPainted(false);
	 btn.setContentAreaFilled(false);
	
}
}
