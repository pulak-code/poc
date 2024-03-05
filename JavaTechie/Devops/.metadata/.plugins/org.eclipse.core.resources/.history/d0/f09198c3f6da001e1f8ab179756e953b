package crud.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import crud.entity.User;
import crud.repo.UserRepository;

@Service
	public class UserService {
	    private final UserRepository userRepository;

	    @Autowired
	    public UserService(UserRepository userRepository) {
	        this.userRepository = userRepository;
	    }

	    public List<User> getAllUsers() {
	        return userRepository.findAll();
	    }

	    public User getUserById(Long id) {
	        return userRepository.findById(id).orElse(null);
	    }

	    public User createUser(User user) {
	        return userRepository.save(user);
	    }

	    public User updateUser(Long id, User updatedUser) {
	        User existingUser = userRepository.findById(id).orElse(null);
	        if (existingUser != null) {
	            // Update fields as needed
	            existingUser.setFirstName(updatedUser.getFirstName());
	            existingUser.setLastName(updatedUser.getLastName());
	            return userRepository.save(existingUser);
	        }
	        return null;
	    }

	    public void deleteUser(Long id) {
	        userRepository.deleteById(id);
	    }
	}
