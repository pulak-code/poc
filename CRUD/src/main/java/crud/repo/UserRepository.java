package crud.repo;

import org.springframework.data.jpa.repository.JpaRepository;

import crud.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
   
}

